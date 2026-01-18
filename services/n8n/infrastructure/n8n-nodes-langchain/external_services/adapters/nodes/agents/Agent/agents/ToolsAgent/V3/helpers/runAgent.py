"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/runAgent.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@langchain/core/…/chat_models、@langchain/classic/agents、@langchain/classic/memory；内部:无；本地:../../prompt、../types、./buildResponseMetadata、./prepareItemContext。导出:无。关键函数/方法:runAgent。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/runAgent.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/runAgent.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import type { AgentRunnableSequence } from '@langchain/classic/agents';
import type { BaseChatMemory } from '@langchain/classic/memory';
import type {
	IExecuteFunctions,
	ISupplyDataFunctions,
	EngineResponse,
	EngineRequest,
} from 'n8n-workflow';

import {
	loadMemory,
	processEventStream,
	createEngineRequests,
	saveToMemory,
} from '@utils/agent-execution';

import { SYSTEM_MESSAGE } from '../../prompt';
import type { AgentResult, RequestResponseMetadata } from '../types';
import { buildResponseMetadata } from './buildResponseMetadata';
import type { ItemContext } from './prepareItemContext';

type RunAgentResult = AgentResult | EngineRequest<RequestResponseMetadata>;
/**
 * Runs the agent for a single item, choosing between streaming or non-streaming execution.
 * Handles both regular execution and execution after tool calls.
 *
 * @param ctx - The execution context
 * @param executor - The agent runnable sequence
 * @param itemContext - Context for the current item
 * @param model - The chat model for token counting
 * @param memory - Optional memory for conversation context
 * @param response - Optional engine response with previous tool calls
 * @returns AgentResult or engine request with tool calls
 */
export async function runAgent(
	ctx: IExecuteFunctions | ISupplyDataFunctions,
	executor: AgentRunnableSequence,
	itemContext: ItemContext,
	model: BaseChatModel,
	memory: BaseChatMemory | undefined,
	response?: EngineResponse<RequestResponseMetadata>,
): Promise<RunAgentResult> {
	const { itemIndex, input, steps, tools, options } = itemContext;

	const invokeParams = {
		steps,
		input,
		system_message: options.systemMessage ?? SYSTEM_MESSAGE,
		formatting_instructions:
			'IMPORTANT: For your response to user, you MUST use the `format_final_json_response` tool with your complete answer formatted according to the required schema. Do not attempt to format the JSON manually - always use this tool. Your response will be rejected if it is not properly formatted through this tool. Only use this tool once you are ready to provide your final answer.',
	};
	const executeOptions = { signal: ctx.getExecutionCancelSignal() };

	// Check if streaming is actually available
	const isStreamingAvailable = 'isStreaming' in ctx ? ctx.isStreaming?.() : undefined;

	if (
		'isStreaming' in ctx &&
		options.enableStreaming &&
		isStreamingAvailable &&
		ctx.getNode().typeVersion >= 2.1
	) {
		const chatHistory = await loadMemory(memory, model, options.maxTokensFromMemory);
		const eventStream = executor.streamEvents(
			{
				...invokeParams,
				chat_history: chatHistory,
			},
			{
				version: 'v2',
				...executeOptions,
			},
		);

		const result = await processEventStream(ctx, eventStream, itemIndex);

		// If result contains tool calls, build the request object like the normal flow
		if (result.toolCalls && result.toolCalls.length > 0) {
			const actions = await createEngineRequests(result.toolCalls, itemIndex, tools);

			return {
				actions,
				metadata: buildResponseMetadata(response, itemIndex),
			};
		}
		// Save conversation to memory including any tool call context
		if (memory && input && result?.output) {
			const previousCount = response?.metadata?.previousRequests?.length;
			await saveToMemory(input, result.output, memory, steps, previousCount);
		}

		if (options.returnIntermediateSteps && steps.length > 0) {
			result.intermediateSteps = steps;
		}

		return result;
	} else {
		// Handle regular execution
		const chatHistory = await loadMemory(memory, model, options.maxTokensFromMemory);

		const modelResponse = await executor.invoke({
			...invokeParams,
			chat_history: chatHistory,
		});

		if ('returnValues' in modelResponse) {
			// Save conversation to memory including any tool call context
			if (memory && input && modelResponse.returnValues.output) {
				const previousCount = response?.metadata?.previousRequests?.length;
				await saveToMemory(input, modelResponse.returnValues.output, memory, steps, previousCount);
			}
			// Include intermediate steps if requested
			const result = { ...modelResponse.returnValues };
			if (options.returnIntermediateSteps && steps.length > 0) {
				result.intermediateSteps = steps;
			}
			return result;
		}

		// If response contains tool calls, we need to return this in the right format
		const actions = await createEngineRequests(modelResponse, itemIndex, tools);

		return {
			actions,
			metadata: buildResponseMetadata(response, itemIndex),
		};
	}
}
