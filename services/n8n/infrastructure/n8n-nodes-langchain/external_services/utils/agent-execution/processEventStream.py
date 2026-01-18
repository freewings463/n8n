"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/agent-execution/processEventStream.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/agent-execution 的执行工具。导入/依赖:外部:@langchain/core/…/event_stream、@langchain/core/…/stream、@langchain/core/messages；内部:n8n-workflow；本地:./types。导出:无。关键函数/方法:processEventStream。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/agent-execution/processEventStream.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/agent-execution/processEventStream.py

import type { StreamEvent } from '@langchain/core/dist/tracers/event_stream';
import type { IterableReadableStream } from '@langchain/core/dist/utils/stream';
import type { AIMessageChunk, MessageContentText } from '@langchain/core/messages';
import type { IExecuteFunctions } from 'n8n-workflow';

import type { AgentResult, ToolCallRequest } from './types';

/**
 * Processes the event stream from a streaming agent execution.
 * Handles streaming chunks, tool calls, and intermediate steps.
 *
 * This is a generalized version that can be used across different agent types
 * (Tools Agent, OpenAI Functions Agent, etc.).
 *
 * @param ctx - The execution context
 * @param eventStream - The stream of events from the agent
 * @param itemIndex - The current item index
 * @returns AgentResult containing output and optional tool calls/steps
 */
export async function processEventStream(
	ctx: IExecuteFunctions,
	eventStream: IterableReadableStream<StreamEvent>,
	itemIndex: number,
): Promise<AgentResult> {
	const agentResult: AgentResult = {
		output: '',
	};

	const toolCalls: ToolCallRequest[] = [];

	ctx.sendChunk('begin', itemIndex);
	for await (const event of eventStream) {
		// Stream chat model tokens as they come in
		switch (event.event) {
			case 'on_chat_model_stream':
				const chunk = event.data?.chunk as AIMessageChunk;
				if (chunk?.content) {
					const chunkContent = chunk.content;
					let chunkText = '';
					if (Array.isArray(chunkContent)) {
						for (const message of chunkContent) {
							if (message?.type === 'text') {
								chunkText += (message as MessageContentText)?.text;
							}
						}
					} else if (typeof chunkContent === 'string') {
						chunkText = chunkContent;
					}
					ctx.sendChunk('item', itemIndex, chunkText);

					agentResult.output += chunkText;
				}
				break;
			case 'on_chat_model_end':
				// Capture full LLM response with tool calls for intermediate steps
				if (event.data) {
					const chatModelData = event.data;
					const output = chatModelData.output;

					// Check if this LLM response contains tool calls
					if (output?.tool_calls && output.tool_calls.length > 0) {
						// Collect tool calls for request building
						for (const toolCall of output.tool_calls) {
							toolCalls.push({
								tool: toolCall.name,
								toolInput: toolCall.args,
								toolCallId: toolCall.id || 'unknown',
								type: toolCall.type || 'tool_call',
								log:
									output.content ||
									`Calling ${toolCall.name} with input: ${JSON.stringify(toolCall.args)}`,
								messageLog: [output],
							});
						}
					}
				}
				break;
			default:
				break;
		}
	}
	ctx.sendChunk('end', itemIndex);

	// Include collected tool calls in the result
	if (toolCalls.length > 0) {
		agentResult.toolCalls = toolCalls;
	}

	return agentResult;
}
