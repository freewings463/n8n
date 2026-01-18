"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainLLM/methods/processItem.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainLLM 的节点。导入/依赖:外部:@langchain/core/…/base、node:assert、@utils/helpers、@utils/output_parsers/N8nOutputParser；内部:n8n-workflow；本地:./chainExecutor、./types。导出:processItem。关键函数/方法:getChatModel、processItem、assert。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainLLM/methods/processItem.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainLLM/methods/processItem.py

import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import { type IExecuteFunctions, NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';
import assert from 'node:assert';

import { getPromptInputByType } from '@utils/helpers';
import { getOptionalOutputParser } from '@utils/output_parsers/N8nOutputParser';

import { executeChain } from './chainExecutor';
import { type MessageTemplate } from './types';

async function getChatModel(
	ctx: IExecuteFunctions,
	index: number = 0,
): Promise<BaseLanguageModel | undefined> {
	const connectedModels = await ctx.getInputConnectionData(NodeConnectionTypes.AiLanguageModel, 0);

	let model;

	if (Array.isArray(connectedModels) && index !== undefined) {
		if (connectedModels.length <= index) {
			return undefined;
		}
		// We get the models in reversed order from the workflow so we need to reverse them again to match the right index
		const reversedModels = [...connectedModels].reverse();
		model = reversedModels[index] as BaseLanguageModel;
	} else {
		model = connectedModels as BaseLanguageModel;
	}

	return model;
}

export const processItem = async (ctx: IExecuteFunctions, itemIndex: number) => {
	const needsFallback = ctx.getNodeParameter('needsFallback', 0, false) as boolean;
	const llm = await getChatModel(ctx, 0);
	assert(llm, 'Please connect a model to the Chat Model input');

	const fallbackLlm = needsFallback ? await getChatModel(ctx, 1) : null;
	if (needsFallback && !fallbackLlm) {
		throw new NodeOperationError(
			ctx.getNode(),
			'Please connect a model to the Fallback Model input or disable the fallback option',
		);
	}

	// Get output parser if configured
	const outputParser = await getOptionalOutputParser(ctx, itemIndex);

	// Get user prompt based on node version
	let prompt: string;

	if (ctx.getNode().typeVersion <= 1.3) {
		prompt = ctx.getNodeParameter('prompt', itemIndex) as string;
	} else {
		prompt = getPromptInputByType({
			ctx,
			i: itemIndex,
			inputKey: 'text',
			promptTypeKey: 'promptType',
		});
	}

	// Validate prompt
	if (prompt === undefined) {
		throw new NodeOperationError(ctx.getNode(), "The 'prompt' parameter is empty.");
	}

	// Get chat messages if configured
	const messages = ctx.getNodeParameter(
		'messages.messageValues',
		itemIndex,
		[],
	) as MessageTemplate[];

	// Execute the chain
	return await executeChain({
		context: ctx,
		itemIndex,
		query: prompt,
		llm,
		outputParser,
		messages,
		fallbackLlm,
	});
};
