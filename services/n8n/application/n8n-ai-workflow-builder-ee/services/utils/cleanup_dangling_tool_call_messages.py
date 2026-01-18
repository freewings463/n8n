"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/cleanup-dangling-tool-call-messages.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:@langchain/core/messages；内部:无；本地:无。导出:cleanupDanglingToolCallMessages。关键函数/方法:cleanupDanglingToolCallMessages。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/cleanup-dangling-tool-call-messages.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/cleanup_dangling_tool_call_messages.py

import type { BaseMessage } from '@langchain/core/messages';
import { AIMessage, RemoveMessage, ToolMessage } from '@langchain/core/messages';

/**
 * In cases where the request was interrupted while a tool call was in progress
 * (e.g. network error), we might end up with dangling tool calls in the state.
 * This function identifies AI messages that have tool calls without corresponding
 * ToolMessage responses and returns RemoveMessage instances to clean them up.
 */
export function cleanupDanglingToolCallMessages(messages: BaseMessage[]): RemoveMessage[] {
	// First we collect all tool call IDs from ToolMessages
	const toolCallIds = new Set(
		messages.filter((m): m is ToolMessage => m instanceof ToolMessage).map((m) => m.tool_call_id),
	);

	// Then we look for AI messages which reference tool calls, but the tool call ID is not in the set
	// (this means the tool call was never completed)
	const danglingToolCalls = messages.filter(
		(m) => m instanceof AIMessage && m.tool_calls?.some(({ id }) => id && !toolCallIds.has(id)),
	);

	// Remove dangling tool calls, as otherwise it will block agent execution
	return danglingToolCalls.map((m) => new RemoveMessage({ id: m.id! }));
}
