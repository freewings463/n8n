"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/messages.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:无；本地:无。导出:QuickReplyOption、AssistantChatMessage、AssistantSummaryMessage、EndSessionMessage、AgentChatMessage、MessageResponse。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。注释目标:Quick reply option for chat messages。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/messages.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/messages.py

/**
 * Quick reply option for chat messages
 */
export interface QuickReplyOption {
	text: string;
	type: string;
	isFeedback?: boolean;
}

/**
 * Assistant chat message
 */
export interface AssistantChatMessage {
	role: 'assistant';
	type: 'message';
	text: string;
	step?: string;
	codeSnippet?: string;
}

/**
 * Assistant summary message
 */
export interface AssistantSummaryMessage {
	role: 'assistant';
	type: 'summary';
	title: string;
	content: string;
}

/**
 * End session event message
 */
export interface EndSessionMessage {
	role: 'assistant';
	type: 'event';
	eventName: 'end-session';
}

/**
 * Agent suggestion message
 */
export interface AgentChatMessage {
	role: 'assistant';
	type: 'agent-suggestion';
	title: string;
	text: string;
}

/**
 * Union type for all possible message responses
 */
export type MessageResponse =
	| ((AssistantChatMessage | AssistantSummaryMessage | AgentChatMessage) & {
			quickReplies?: QuickReplyOption[];
	  })
	| EndSessionMessage;
