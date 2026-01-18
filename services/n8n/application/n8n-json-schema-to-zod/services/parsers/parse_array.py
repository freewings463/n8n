"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-array.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:./parse-schema、../types、../utils/extend-schema。导出:parseArray。关键函数/方法:parseArray、parseSchema。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-array.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_array.py

import { z } from 'zod';

import { parseSchema } from './parse-schema';
import type { JsonSchemaObject, Refs } from '../types';
import { extendSchemaWithMessage } from '../utils/extend-schema';

export const parseArray = (jsonSchema: JsonSchemaObject & { type: 'array' }, refs: Refs) => {
	if (Array.isArray(jsonSchema.items)) {
		return z.tuple(
			jsonSchema.items.map((v, i) =>
				parseSchema(v, { ...refs, path: [...refs.path, 'items', i] }),
			) as [z.ZodTypeAny],
		);
	}

	let zodSchema = !jsonSchema.items
		? z.array(z.any())
		: z.array(parseSchema(jsonSchema.items, { ...refs, path: [...refs.path, 'items'] }));

	zodSchema = extendSchemaWithMessage(
		zodSchema,
		jsonSchema,
		'minItems',
		(zs, minItems, errorMessage) => zs.min(minItems, errorMessage),
	);
	zodSchema = extendSchemaWithMessage(
		zodSchema,
		jsonSchema,
		'maxItems',
		(zs, maxItems, errorMessage) => zs.max(maxItems, errorMessage),
	);

	return zodSchema;
};
