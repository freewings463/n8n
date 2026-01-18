"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/utils/extend-schema.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/utils 的工具。导入/依赖:外部:zod；内部:无；本地:../types。导出:extendSchemaWithMessage。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/utils/extend-schema.ts -> services/n8n/application/n8n-json-schema-to-zod/services/utils/extend_schema.py

import type { z } from 'zod';

import type { JsonSchemaObject } from '../types';

export function extendSchemaWithMessage<
	TZod extends z.ZodTypeAny,
	TJson extends JsonSchemaObject,
	TKey extends keyof TJson,
>(
	zodSchema: TZod,
	jsonSchema: TJson,
	key: TKey,
	extend: (zodSchema: TZod, value: NonNullable<TJson[TKey]>, errorMessage?: string) => TZod,
) {
	const value = jsonSchema[key];

	if (value !== undefined) {
		const errorMessage = jsonSchema.errorMessage?.[key as string];
		return extend(zodSchema, value as NonNullable<TJson[TKey]>, errorMessage);
	}

	return zodSchema;
}
