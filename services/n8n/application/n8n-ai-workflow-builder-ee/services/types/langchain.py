"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/langchain.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:@langchain/core/messages；内部:无；本地:无。导出:isAIMessage、isBaseMessage。关键函数/方法:isAIMessage、isBaseMessage、typeof。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/langchain.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/langchain.py

import type { AIMessage, BaseMessage } from '@langchain/core/messages';

export function isAIMessage(msg: BaseMessage): msg is AIMessage {
	return msg.getType() === 'ai';
}

/**
 * Type guard to check if a value is a BaseMessage
 * BaseMessage instances have a getType method and content property
 */
export function isBaseMessage(value: unknown): value is BaseMessage {
	return (
		typeof value === 'object' &&
		value !== null &&
		'getType' in value &&
		typeof (value as { getType: unknown }).getType === 'function' &&
		'content' in value
	);
}
