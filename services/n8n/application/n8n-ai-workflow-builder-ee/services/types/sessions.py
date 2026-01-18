"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/sessions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:@langchain/core/messages；内部:无；本地:无。导出:Session、LangchainMessage、isLangchainMessagesArray。关键函数/方法:isLangchainMessage、isLangchainMessagesArray。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/sessions.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/sessions.py

import type { AIMessage, HumanMessage, ToolMessage } from '@langchain/core/messages';

export interface Session {
	sessionId: string;
	messages: Array<Record<string, unknown>>;
	lastUpdated?: string;
}

export type LangchainMessage = AIMessage | HumanMessage | ToolMessage;

/**
 * Type guard to validate if a value is a valid Langchain message
 */
function isLangchainMessage(value: unknown): value is LangchainMessage {
	if (!value || typeof value !== 'object') {
		return false;
	}

	// Check for required properties that all message types have
	if (!('content' in value)) {
		return false;
	}

	const content = value.content;
	if (typeof content !== 'string' && !Array.isArray(content)) {
		return false;
	}

	// Check for message type indicators
	const hasValidType =
		'_getType' in value || // Common method in Langchain messages
		('constructor' in value &&
			value.constructor !== null &&
			typeof value.constructor === 'function' &&
			'name' in value.constructor &&
			(value.constructor.name === 'AIMessage' ||
				value.constructor.name === 'HumanMessage' ||
				value.constructor.name === 'ToolMessage')) ||
		('role' in value &&
			typeof value.role === 'string' &&
			['assistant', 'human', 'user', 'tool'].includes(value.role));

	return hasValidType;
}

/**
 * Type guard to validate if a value is an array of Langchain messages
 */
export function isLangchainMessagesArray(value: unknown): value is LangchainMessage[] {
	if (!Array.isArray(value)) {
		return false;
	}

	return value.every(isLangchainMessage);
}
