"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/checkMaxIterations.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../types。导出:checkMaxIterations。关键函数/方法:checkMaxIterations。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/checkMaxIterations.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/checkMaxIterations.py

import { NodeOperationError } from 'n8n-workflow';
import type { INode, EngineResponse } from 'n8n-workflow';

import type { RequestResponseMetadata } from '../types';

/**
 * Checks if the maximum iteration limit has been reached and throws an error if so.
 *
 * This function is called at the start of each agent execution to enforce
 * the maximum number of tool call iterations allowed.
 *
 * @param response - The engine response containing iteration metadata (if this is a continuation)
 * @param maxIterations - The maximum number of iterations allowed
 * @param node - The current node (for error context)
 * @throws {NodeOperationError} When the iteration count reaches or exceeds maxIterations
 *
 * @example
 * ```typescript
 * const response: EngineResponse<RequestResponseMetadata> = {
 *   // ... response data
 *   metadata: { iterationCount: 3 }
 * };
 *
 * // This will throw if iterationCount >= maxIterations
 * checkMaxIterations(response, 2, node);
 * ```
 */
export function checkMaxIterations(
	response: EngineResponse<RequestResponseMetadata> | undefined,
	maxIterations: number,
	node: INode,
): void {
	// Only check if this is a continuation (response has iteration count)
	if (response?.metadata?.iterationCount === undefined) {
		return;
	}

	if (response.metadata.iterationCount >= maxIterations) {
		throw new NodeOperationError(
			node,
			`Max iterations (${maxIterations}) reached. The agent could not complete the task within the allowed number of iterations.`,
		);
	}
}
