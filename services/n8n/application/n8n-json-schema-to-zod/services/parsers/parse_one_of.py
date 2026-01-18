"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-one-of.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:./parse-schema、../types。导出:parseOneOf。关键函数/方法:parseOneOf、parseSchema。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-one-of.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_one_of.py

import { z } from 'zod';

import { parseSchema } from './parse-schema';
import type { JsonSchemaObject, JsonSchema, Refs } from '../types';

export const parseOneOf = (jsonSchema: JsonSchemaObject & { oneOf: JsonSchema[] }, refs: Refs) => {
	if (!jsonSchema.oneOf.length) {
		return z.any();
	}

	if (jsonSchema.oneOf.length === 1) {
		return parseSchema(jsonSchema.oneOf[0], {
			...refs,
			path: [...refs.path, 'oneOf', 0],
		});
	}

	return z.any().superRefine((x, ctx) => {
		const schemas = jsonSchema.oneOf.map((schema, i) =>
			parseSchema(schema, {
				...refs,
				path: [...refs.path, 'oneOf', i],
			}),
		);

		const unionErrors = schemas.reduce<z.ZodError[]>(
			(errors, schema) =>
				((result) => (result.error ? [...errors, result.error] : errors))(schema.safeParse(x)),
			[],
		);

		if (schemas.length - unionErrors.length !== 1) {
			ctx.addIssue({
				path: ctx.path,
				code: 'invalid_union',
				unionErrors,
				message: 'Invalid input: Should pass single schema',
			});
		}
	});
};
