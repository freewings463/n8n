"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-null.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:../types。导出:parseNull。关键函数/方法:parseNull。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-null.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_null.py

import { z } from 'zod';

import type { JsonSchemaObject } from '../types';

export const parseNull = (_jsonSchema: JsonSchemaObject & { type: 'null' }) => {
	return z.null();
};
