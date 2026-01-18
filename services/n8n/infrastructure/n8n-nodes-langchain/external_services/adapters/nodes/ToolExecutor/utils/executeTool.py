"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/ToolExecutor/utils/executeTool.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/ToolExecutor/utils 的工具。导入/依赖:外部:@langchain/core/tools；内部:n8n-workflow；本地:./convertToSchema。导出:无。关键函数/方法:executeTool。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/ToolExecutor/utils/executeTool.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/ToolExecutor/utils/executeTool.py

import type { Tool } from '@langchain/core/tools';
import { type IDataObject, type INodeExecutionData } from 'n8n-workflow';

import { convertObjectBySchema } from './convertToSchema';

export async function executeTool(tool: Tool, query: string | object): Promise<INodeExecutionData> {
	let convertedQuery: string | object = query;
	if ('schema' in tool && tool.schema) {
		convertedQuery = convertObjectBySchema(query, tool.schema);
	}

	const result = await tool.invoke(convertedQuery);

	return {
		json: result as IDataObject,
	};
}
