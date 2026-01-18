"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/ToolExecutor/utils/convertToSchema.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/ToolExecutor/utils 的工具。导入/依赖:外部:zod；内部:无；本地:无。导出:convertValueBySchema、convertObjectBySchema。关键函数/方法:convertValueBySchema、convertObjectBySchema。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/ToolExecutor/utils/convertToSchema.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/ToolExecutor/utils/convertToSchema.py

import { z } from 'zod';

export const convertValueBySchema = (value: unknown, schema: any): unknown => {
	if (!schema || !value) return value;

	if (typeof value === 'string') {
		if (schema instanceof z.ZodNumber) {
			return Number(value);
		} else if (schema instanceof z.ZodBoolean) {
			return value.toLowerCase() === 'true';
		} else if (schema instanceof z.ZodObject) {
			try {
				const parsed = JSON.parse(value);
				return convertValueBySchema(parsed, schema);
			} catch {
				return value;
			}
		}
	}

	if (schema instanceof z.ZodObject && typeof value === 'object' && value !== null) {
		const result: any = {};
		for (const [key, val] of Object.entries(value)) {
			const fieldSchema = schema.shape[key];
			if (fieldSchema) {
				result[key] = convertValueBySchema(val, fieldSchema);
			} else {
				result[key] = val;
			}
		}
		return result;
	}

	return value;
};

export const convertObjectBySchema = (obj: any, schema: any): any => {
	return convertValueBySchema(obj, schema);
};
