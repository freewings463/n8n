"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/buildResponseMetadata.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@utils/agent-execution；内部:n8n-workflow；本地:../types。导出:buildResponseMetadata。关键函数/方法:buildResponseMetadata。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/buildResponseMetadata.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/buildResponseMetadata.py

import type { EngineResponse } from 'n8n-workflow';

import { buildSteps } from '@utils/agent-execution';

import type { RequestResponseMetadata } from '../types';

/**
 * Builds metadata for an engine request, tracking iteration count and previous requests.
 *
 * This helper centralizes the logic for incrementing iteration count and building
 * the request history, which is used to enforce max iterations and maintain context.
 *
 * @param response - The optional engine response from previous tool execution
 * @param itemIndex - The current item index being processed
 * @returns Metadata object with previousRequests and iterationCount
 *
 */
export function buildResponseMetadata(
	response: EngineResponse<RequestResponseMetadata> | undefined,
	itemIndex: number,
): RequestResponseMetadata {
	const currentIterationCount = response?.metadata?.iterationCount ?? 0;

	return {
		previousRequests: buildSteps(response, itemIndex),
		itemIndex,
		iterationCount: currentIterationCount + 1,
	};
}
