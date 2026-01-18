"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/agent-execution/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/agent-execution 的执行工具。导入/依赖:外部:@langchain/core/messages；内部:n8n-workflow；本地:无。导出:ToolCallRequest、ToolCallData、AgentResult、ThinkingContentBlock、RedactedThinkingContentBlock、ToolUseContentBlock、GeminiThoughtSignatureBlock、ContentBlock 等4项。关键函数/方法:isThinkingBlock、isRedactedThinkingBlock、isGeminiThoughtSignatureBlock。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/agent-execution/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/agent-execution/types.py

import type { AIMessage } from '@langchain/core/messages';
import type { IDataObject, GenericValue } from 'n8n-workflow';

/**
 * Represents a tool call request from an LLM.
 * This is a generic format that can be used across different agent types.
 */
export type ToolCallRequest = {
	/** The name of the tool to call */
	tool: string;
	/** The input arguments for the tool */
	toolInput: Record<string, unknown>;
	/** Unique identifier for this tool call */
	toolCallId: string;
	/** Type of the tool call (e.g., 'tool_call', 'function') */
	type?: string;
	/** Log message or description */
	log?: string;
	/** Full message log including LLM response */
	messageLog?: unknown[];
};

/**
 * Represents a tool call action and its observation result.
 * Used for building agent steps and maintaining conversation context.
 */
export type ToolCallData = {
	action: {
		tool: string;
		toolInput: Record<string, unknown>;
		log: string | number | true | object;
		messageLog?: AIMessage[];
		toolCallId: IDataObject | GenericValue | GenericValue[] | IDataObject[];
		type: string | number | true | object;
	};
	observation: string;
};

/**
 * Result from an agent execution, optionally including tool calls and intermediate steps.
 */
export type AgentResult = {
	/** The final output from the agent */
	output: string;
	/** Tool calls that need to be executed */
	toolCalls?: ToolCallRequest[];
	/** Intermediate steps showing the agent's reasoning */
	intermediateSteps?: ToolCallData[];
};

/**
 * Anthropic thinking content block
 */
export type ThinkingContentBlock = {
	type: 'thinking';
	thinking: string;
	signature: string;
};

/**
 * Anthropic redacted thinking content block
 */
export type RedactedThinkingContentBlock = {
	type: 'redacted_thinking';
	data: string;
};

/**
 * Anthropic tool use content block
 */
export type ToolUseContentBlock = {
	type: 'tool_use';
	id: string;
	name: string;
	input: Record<string, unknown>;
};

/**
 * Gemini thought signature content block
 */
export type GeminiThoughtSignatureBlock = {
	thoughtSignature: string;
};

/**
 * Union type for all supported content blocks
 */
export type ContentBlock =
	| ThinkingContentBlock
	| RedactedThinkingContentBlock
	| ToolUseContentBlock
	| GeminiThoughtSignatureBlock;

/**
 * Metadata for engine requests and responses.
 */
export type RequestResponseMetadata = {
	/** Item index being processed */
	itemIndex?: number;
	/** Previous tool call requests (for multi-turn conversations) */
	previousRequests?: ToolCallData[];
	/** Current iteration count (for max iterations enforcement) */
	iterationCount?: number;
	/** Google/Gemini-specific metadata */
	google?: {
		/** Thought signature for Gemini extended thinking */
		thoughtSignature?: string;
	};
	/** Anthropic-specific metadata */
	anthropic?: {
		/** Thinking content from extended thinking mode */
		thinkingContent?: string;
		/** Type of thinking block (thinking or redacted_thinking) */
		thinkingType?: 'thinking' | 'redacted_thinking';
		/** Cryptographic signature for thinking blocks */
		thinkingSignature?: string;
	};
};

/**
 * Type guard to check if a block is a thinking content block
 */
export function isThinkingBlock(block: unknown): block is ThinkingContentBlock {
	return (
		typeof block === 'object' &&
		block !== null &&
		'type' in block &&
		block.type === 'thinking' &&
		'thinking' in block &&
		typeof block.thinking === 'string' &&
		'signature' in block &&
		typeof block.signature === 'string'
	);
}

/**
 * Type guard to check if a block is a redacted thinking content block
 */
export function isRedactedThinkingBlock(block: unknown): block is RedactedThinkingContentBlock {
	return (
		typeof block === 'object' &&
		block !== null &&
		'type' in block &&
		block.type === 'redacted_thinking' &&
		'data' in block &&
		typeof block.data === 'string'
	);
}

/**
 * Type guard to check if a block is a Gemini thought signature block
 */
export function isGeminiThoughtSignatureBlock(
	block: unknown,
): block is GeminiThoughtSignatureBlock {
	return (
		typeof block === 'object' &&
		block !== null &&
		'thoughtSignature' in block &&
		typeof block.thoughtSignature === 'string'
	);
}
