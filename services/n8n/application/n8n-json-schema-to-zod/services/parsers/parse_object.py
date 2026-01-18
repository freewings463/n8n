"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-object.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:./parse-all-of、./parse-any-of、./parse-one-of、./parse-schema 等2项。导出:parseObject。关键函数/方法:parseObjectProperties、parseObject、parseSchema、parseAnyOf、parseOneOf、parseAllOf。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-object.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_object.py

import * as z from 'zod';

import { parseAllOf } from './parse-all-of';
import { parseAnyOf } from './parse-any-of';
import { parseOneOf } from './parse-one-of';
import { parseSchema } from './parse-schema';
import type { JsonSchemaObject, Refs } from '../types';
import { its } from '../utils/its';

function parseObjectProperties(objectSchema: JsonSchemaObject & { type: 'object' }, refs: Refs) {
	if (!objectSchema.properties) {
		return undefined;
	}

	const propertyKeys = Object.keys(objectSchema.properties);
	if (propertyKeys.length === 0) {
		return z.object({});
	}

	const properties: Record<string, z.ZodTypeAny> = {};

	for (const key of propertyKeys) {
		const propJsonSchema = objectSchema.properties[key];

		const propZodSchema = parseSchema(propJsonSchema, {
			...refs,
			path: [...refs.path, 'properties', key],
		});

		const hasDefault = typeof propJsonSchema === 'object' && propJsonSchema.default !== undefined;

		const required = Array.isArray(objectSchema.required)
			? objectSchema.required.includes(key)
			: typeof propJsonSchema === 'object' && propJsonSchema.required === true;

		const isOptional = !hasDefault && !required;

		properties[key] = isOptional ? propZodSchema.optional() : propZodSchema;
	}

	return z.object(properties);
}

export function parseObject(
	objectSchema: JsonSchemaObject & { type: 'object' },
	refs: Refs,
): z.ZodTypeAny {
	const hasPatternProperties = Object.keys(objectSchema.patternProperties ?? {}).length > 0;

	const propertiesSchema:
		| z.ZodObject<Record<string, z.ZodTypeAny>, 'strip', z.ZodTypeAny>
		| undefined = parseObjectProperties(objectSchema, refs);
	let zodSchema: z.ZodTypeAny | undefined = propertiesSchema;

	const additionalProperties =
		objectSchema.additionalProperties !== undefined
			? parseSchema(objectSchema.additionalProperties, {
					...refs,
					path: [...refs.path, 'additionalProperties'],
				})
			: undefined;

	if (objectSchema.patternProperties) {
		const parsedPatternProperties = Object.fromEntries(
			Object.entries(objectSchema.patternProperties).map(([key, value]) => {
				return [
					key,
					parseSchema(value, {
						...refs,
						path: [...refs.path, 'patternProperties', key],
					}),
				];
			}),
		);
		const patternPropertyValues = Object.values(parsedPatternProperties);

		if (propertiesSchema) {
			if (additionalProperties) {
				zodSchema = propertiesSchema.catchall(
					z.union([...patternPropertyValues, additionalProperties] as [z.ZodTypeAny, z.ZodTypeAny]),
				);
			} else if (Object.keys(parsedPatternProperties).length > 1) {
				zodSchema = propertiesSchema.catchall(
					z.union(patternPropertyValues as [z.ZodTypeAny, z.ZodTypeAny]),
				);
			} else {
				zodSchema = propertiesSchema.catchall(patternPropertyValues[0]);
			}
		} else {
			if (additionalProperties) {
				zodSchema = z.record(
					z.union([...patternPropertyValues, additionalProperties] as [z.ZodTypeAny, z.ZodTypeAny]),
				);
			} else if (patternPropertyValues.length > 1) {
				zodSchema = z.record(z.union(patternPropertyValues as [z.ZodTypeAny, z.ZodTypeAny]));
			} else {
				zodSchema = z.record(patternPropertyValues[0]);
			}
		}

		const objectPropertyKeys = new Set(Object.keys(objectSchema.properties ?? {}));
		zodSchema = zodSchema.superRefine((value: Record<string, unknown>, ctx) => {
			for (const key in value) {
				let wasMatched = objectPropertyKeys.has(key);

				for (const patternPropertyKey in objectSchema.patternProperties) {
					const regex = new RegExp(patternPropertyKey);
					if (key.match(regex)) {
						wasMatched = true;
						const result = parsedPatternProperties[patternPropertyKey].safeParse(value[key]);
						if (!result.success) {
							ctx.addIssue({
								path: [...ctx.path, key],
								code: 'custom',
								message: `Invalid input: Key matching regex /${key}/ must match schema`,
								params: {
									issues: result.error.issues,
								},
							});
						}
					}
				}

				if (!wasMatched && additionalProperties) {
					const result = additionalProperties.safeParse(value[key]);
					if (!result.success) {
						ctx.addIssue({
							path: [...ctx.path, key],
							code: 'custom',
							message: 'Invalid input: must match catchall schema',
							params: {
								issues: result.error.issues,
							},
						});
					}
				}
			}
		});
	}

	let output: z.ZodTypeAny;
	if (propertiesSchema) {
		if (hasPatternProperties) {
			output = zodSchema!;
		} else if (additionalProperties) {
			if (additionalProperties instanceof z.ZodNever) {
				output = propertiesSchema.strict();
			} else {
				output = propertiesSchema.catchall(additionalProperties);
			}
		} else {
			output = zodSchema!;
		}
	} else {
		if (hasPatternProperties) {
			output = zodSchema!;
		} else if (additionalProperties) {
			output = z.record(additionalProperties);
		} else {
			output = z.record(z.any());
		}
	}

	if (its.an.anyOf(objectSchema)) {
		output = output.and(
			parseAnyOf(
				{
					...objectSchema,
					anyOf: objectSchema.anyOf.map((x) =>
						typeof x === 'object' &&
						!x.type &&
						(x.properties ?? x.additionalProperties ?? x.patternProperties)
							? { ...x, type: 'object' }
							: x,
					),
				},
				refs,
			),
		);
	}

	if (its.a.oneOf(objectSchema)) {
		output = output.and(
			parseOneOf(
				{
					...objectSchema,
					oneOf: objectSchema.oneOf.map((x) =>
						typeof x === 'object' &&
						!x.type &&
						(x.properties ?? x.additionalProperties ?? x.patternProperties)
							? { ...x, type: 'object' }
							: x,
					),
				},
				refs,
			),
		);
	}

	if (its.an.allOf(objectSchema)) {
		output = output.and(
			parseAllOf(
				{
					...objectSchema,
					allOf: objectSchema.allOf.map((x) =>
						typeof x === 'object' &&
						!x.type &&
						(x.properties ?? x.additionalProperties ?? x.patternProperties)
							? { ...x, type: 'object' }
							: x,
					),
				},
				refs,
			),
		);
	}

	return output;
}
