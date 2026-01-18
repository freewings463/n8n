"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-nullable.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:无；内部:无；本地:./parse-schema、../types、../utils/omit。导出:parseNullable。关键函数/方法:parseNullable。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-nullable.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_nullable.py

import { parseSchema } from './parse-schema';
import type { JsonSchemaObject, Refs } from '../types';
import { omit } from '../utils/omit';

/**
 * For compatibility with open api 3.0 nullable
 */
export const parseNullable = (jsonSchema: JsonSchemaObject & { nullable: true }, refs: Refs) => {
	return parseSchema(omit(jsonSchema, 'nullable'), refs, true).nullable();
};
