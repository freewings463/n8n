"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/buildExecutionContext.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的执行节点。导入/依赖:外部:@langchain/core/…/chat_models、@langchain/classic/memory、node:assert；内部:n8n-workflow；本地:../../common。导出:ToolsAgentExecutionContext。关键函数/方法:buildToolsAgentExecutionContext、assert。用于实现 n8n 执行节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/buildExecutionContext.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/buildExecutionContext.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import type { BaseChatMemory } from '@langchain/classic/memory';
import { NodeOperationError } from 'n8n-workflow';
import type { IExecuteFunctions, ISupplyDataFunctions, INodeExecutionData } from 'n8n-workflow';
import assert from 'node:assert';

import { getChatModel, getOptionalMemory } from '../../common';

/**
 * Execution context that contains shared configuration needed across all items
 */
export type ToolsAgentExecutionContext = {
	items: INodeExecutionData[];
	batchSize: number;
	delayBetweenBatches: number;
	needsFallback: boolean;
	model: BaseChatModel;
	fallbackModel: BaseChatModel | null;
	memory: BaseChatMemory | undefined;
};

/**
 * Builds the execution context by collecting shared configuration
 * such as models, memory, batching settings, and streaming flags.
 *
 * @param ctx - The execution context (IExecuteFunctions or ISupplyDataFunctions)
 * @returns ExecutionContext containing all shared configuration
 */
export async function buildToolsAgentExecutionContext(
	ctx: IExecuteFunctions | ISupplyDataFunctions,
): Promise<ToolsAgentExecutionContext> {
	const items = ctx.getInputData();
	const batchSize = ctx.getNodeParameter('options.batching.batchSize', 0, 1) as number;
	const delayBetweenBatches = ctx.getNodeParameter(
		'options.batching.delayBetweenBatches',
		0,
		0,
	) as number;
	const needsFallback = ctx.getNodeParameter('needsFallback', 0, false) as boolean;

	const memory = await getOptionalMemory(ctx);
	const model = await getChatModel(ctx, 0);
	assert(model, 'Please connect a model to the Chat Model input');

	let fallbackModel: BaseChatModel | null = null;
	if (needsFallback) {
		const maybeFallbackModel = await getChatModel(ctx, 1);
		if (!maybeFallbackModel) {
			throw new NodeOperationError(
				ctx.getNode(),
				'Please connect a model to the Fallback Model input or disable the fallback option',
			);
		}
		fallbackModel = maybeFallbackModel;
	}

	return {
		items,
		batchSize,
		delayBetweenBatches,
		needsFallback,
		model,
		fallbackModel,
		memory,
	};
}
