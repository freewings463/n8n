"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-if-then-else.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:./parse-schema、../types。导出:parseIfThenElse。关键函数/方法:parseIfThenElse。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-if-then-else.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_if_then_else.py

import { z } from 'zod';

import { parseSchema } from './parse-schema';
import type { JsonSchemaObject, JsonSchema, Refs } from '../types';

export const parseIfThenElse = (
	jsonSchema: JsonSchemaObject & {
		if: JsonSchema;
		then: JsonSchema;
		else: JsonSchema;
	},
	refs: Refs,
) => {
	const $if = parseSchema(jsonSchema.if, { ...refs, path: [...refs.path, 'if'] });
	const $then = parseSchema(jsonSchema.then, {
		...refs,
		path: [...refs.path, 'then'],
	});
	const $else = parseSchema(jsonSchema.else, {
		...refs,
		path: [...refs.path, 'else'],
	});

	return z.union([$then, $else]).superRefine((value, ctx) => {
		const result = $if.safeParse(value).success ? $then.safeParse(value) : $else.safeParse(value);

		if (!result.success) {
			result.error.errors.forEach((error) => ctx.addIssue(error));
		}
	});
};
