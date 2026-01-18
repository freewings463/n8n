"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-multiple-type.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:./parse-schema、../types。导出:parseMultipleType。关键函数/方法:parseMultipleType。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-multiple-type.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_multiple_type.py

import { z } from 'zod';

import { parseSchema } from './parse-schema';
import type { JsonSchema, JsonSchemaObject, Refs } from '../types';

export const parseMultipleType = (
	jsonSchema: JsonSchemaObject & { type: string[] },
	refs: Refs,
) => {
	return z.union(
		jsonSchema.type.map((type) => parseSchema({ ...jsonSchema, type } as JsonSchema, refs)) as [
			z.ZodTypeAny,
			z.ZodTypeAny,
		],
	);
};
