"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./helpers、./types。导出:无。关键函数/方法:toolsAgentExecute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/execute.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/execute.py

import { sleep } from 'n8n-workflow';
import type {
	EngineRequest,
	IExecuteFunctions,
	INodeExecutionData,
	ISupplyDataFunctions,
	EngineResponse,
} from 'n8n-workflow';

import { buildExecutionContext, executeBatch } from './helpers';
import type { RequestResponseMetadata } from './types';

/* -----------------------------------------------------------
   Main Executor Function
----------------------------------------------------------- */
/**
 * The main executor method for the Tools Agent V3.
 *
 * This function orchestrates the execution across input batches, handling:
 * - Building shared execution context (models, memory, batching config)
 * - Processing items in batches with continue-on-fail logic
 * - Returning either tool call requests or node output data
 *
 * @param this Execute context. SupplyDataContext is passed when agent is used as a tool
 * @param response Optional engine response containing tool call results from previous execution
 * @returns Array of execution data for all processed items, or engine request for tool calls
 */
export async function toolsAgentExecute(
	this: IExecuteFunctions | ISupplyDataFunctions,
	response?: EngineResponse<RequestResponseMetadata>,
): Promise<INodeExecutionData[][] | EngineRequest<RequestResponseMetadata>> {
	this.logger.debug('Executing Tools Agent V3');

	let request: EngineRequest<RequestResponseMetadata> | undefined = undefined;

	const returnData: INodeExecutionData[] = [];

	// Build execution context with shared configuration
	const executionContext = await buildExecutionContext(this);
	const { items, batchSize, delayBetweenBatches, model, fallbackModel, memory } = executionContext;

	// Process items in batches
	for (let i = 0; i < items.length; i += batchSize) {
		const batch = items.slice(i, i + batchSize);

		const { returnData: batchReturnData, request: batchRequest } = await executeBatch(
			this,
			batch,
			i,
			model,
			fallbackModel,
			memory,
			response,
		);

		// Collect results from batch
		returnData.push.apply(returnData, batchReturnData);

		// Collect requests from batch
		if (batchRequest) {
			if (!request) {
				request = batchRequest;
			} else {
				request.actions.push.apply(request.actions, batchRequest.actions);
			}
		}

		// Apply delay between batches if configured
		if (i + batchSize < items.length && delayBetweenBatches > 0) {
			await sleep(delayBetweenBatches);
		}
	}

	// Return tool call request if any tools need to be executed
	if (request) {
		return request;
	}

	// Otherwise return execution data
	return [returnData];
}

// Re-export types for backwards compatibility
export type { RequestResponseMetadata } from './types';
