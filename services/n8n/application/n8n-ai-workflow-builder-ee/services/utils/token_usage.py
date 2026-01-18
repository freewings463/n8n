"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/token-usage.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:@langchain/core/messages；内部:@/constants；本地:无。导出:AIMessageWithUsageMetadata、TokenUsage、extractLastTokenUsage、estimateTokenCountFromString、estimateTokenCountFromMessages。关键函数/方法:extractLastTokenUsage、concatenateMessageContent、estimateTokenCountFromString、estimateTokenCountFromMessages。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/token-usage.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/token_usage.py

import type { BaseMessage } from '@langchain/core/messages';
import { AIMessage } from '@langchain/core/messages';

import { AVG_CHARS_PER_TOKEN_ANTHROPIC } from '@/constants';

export type AIMessageWithUsageMetadata = AIMessage & {
	response_metadata: {
		usage: {
			input_tokens: number;
			output_tokens: number;
			cache_read_input_tokens?: number;
			cache_creation_input_tokens?: number;
		};
	};
};

export interface TokenUsage {
	input_tokens: number;
	output_tokens: number;
	cache_read_input_tokens?: number;
	cache_creation_input_tokens?: number;
}

/**
 * Extracts token usage information from the last AI assistant message
 */
export function extractLastTokenUsage(messages: unknown[]): TokenUsage | undefined {
	const lastAiAssistantMessage = messages.findLast(
		(m): m is AIMessageWithUsageMetadata =>
			m instanceof AIMessage &&
			m.response_metadata?.usage !== undefined &&
			'input_tokens' in m.response_metadata.usage &&
			'output_tokens' in m.response_metadata.usage,
	);

	if (!lastAiAssistantMessage) {
		return undefined;
	}

	return lastAiAssistantMessage.response_metadata.usage;
}

function concatenateMessageContent(messages: BaseMessage[]): string {
	return messages.reduce((acc: string, message) => {
		if (typeof message.content === 'string') {
			return acc + message.content;
		} else if (Array.isArray(message.content)) {
			return (
				acc +
				message.content.reduce((innerAcc: string, item) => {
					if (
						typeof item === 'object' &&
						item !== null &&
						'text' in item &&
						typeof item.text === 'string'
					) {
						return innerAcc + item.text;
					}
					return innerAcc;
				}, '')
			);
		}
		return acc;
	}, '');
}

export function estimateTokenCountFromString(text: string): number {
	return Math.ceil(text.length / AVG_CHARS_PER_TOKEN_ANTHROPIC); // Rough estimate
}

export function estimateTokenCountFromMessages(messages: BaseMessage[]): number {
	const entireInput = concatenateMessageContent(messages);

	return estimateTokenCountFromString(entireInput);
}
