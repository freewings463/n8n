"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/prepareItemContext.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@langchain/core/prompts、@langchain/classic/tools、@utils/agent-execution、@utils/helpers、@utils/output_parsers/N8nOutputParser；内部:n8n-workflow；本地:../../common、../types。导出:ItemContext。关键函数/方法:prepareItemContext。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/prepareItemContext.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/prepareItemContext.py

import type { ChatPromptTemplate } from '@langchain/core/prompts';
import type { DynamicStructuredTool, Tool } from '@langchain/classic/tools';
import { NodeOperationError } from 'n8n-workflow';
import type { IExecuteFunctions, ISupplyDataFunctions, EngineResponse } from 'n8n-workflow';

import { buildSteps, type ToolCallData } from '@utils/agent-execution';
import { getPromptInputByType } from '@utils/helpers';
import { getOptionalOutputParser } from '@utils/output_parsers/N8nOutputParser';
import type { N8nOutputParser } from '@utils/output_parsers/N8nOutputParser';

import { getTools, prepareMessages, preparePrompt } from '../../common';
import type { AgentOptions, RequestResponseMetadata } from '../types';

/**
 * Context specific to a single item's processing
 */
export type ItemContext = {
	itemIndex: number;
	input: string;
	steps: ToolCallData[];
	tools: Array<DynamicStructuredTool | Tool>;
	prompt: ChatPromptTemplate;
	options: AgentOptions;
	outputParser: N8nOutputParser | undefined;
};

/**
 * Prepares the context for processing a single item.
 * This includes loading steps, input, tools, prompt, and options.
 *
 * @param ctx - The execution context
 * @param itemIndex - The index of the item to process
 * @param response - Optional engine response with previous tool calls
 * @returns ItemContext containing all item-specific state
 */
export async function prepareItemContext(
	ctx: IExecuteFunctions | ISupplyDataFunctions,
	itemIndex: number,
	response?: EngineResponse<RequestResponseMetadata>,
): Promise<ItemContext> {
	const steps = buildSteps(response, itemIndex);

	const input = getPromptInputByType({
		ctx,
		i: itemIndex,
		inputKey: 'text',
		promptTypeKey: 'promptType',
	});
	if (input === undefined) {
		throw new NodeOperationError(ctx.getNode(), 'The "text" parameter is empty.');
	}

	const outputParser = await getOptionalOutputParser(ctx, itemIndex);
	const tools = await getTools(ctx, outputParser);
	const options = ctx.getNodeParameter('options', itemIndex) as AgentOptions;

	if (options.enableStreaming === undefined) {
		options.enableStreaming = true;
	}

	// Prepare the prompt messages and prompt template.
	const messages = await prepareMessages(ctx, itemIndex, {
		systemMessage: options.systemMessage,
		passthroughBinaryImages: options.passthroughBinaryImages ?? true,
		outputParser,
	});
	const prompt: ChatPromptTemplate = preparePrompt(messages);

	return {
		itemIndex,
		input,
		steps,
		tools,
		prompt,
		options,
		outputParser,
	};
}
