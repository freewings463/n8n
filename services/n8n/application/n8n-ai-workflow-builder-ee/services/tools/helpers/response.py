"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/helpers/response.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/helpers 的工作流模块。导入/依赖:外部:@langchain/core/messages、@langchain/core/tools、@langchain/langgraph；内部:无；本地:../types/tools、../types/utils、../../workflow-state。导出:createSuccessResponse、createErrorResponse。关键函数/方法:createErrorResponse。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/helpers/response.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/helpers/response.py

import { ToolMessage } from '@langchain/core/messages';
import type { ToolRunnableConfig } from '@langchain/core/tools';
import { Command } from '@langchain/langgraph';

import type { ToolError } from '../../types/tools';
import type { StateUpdater } from '../../types/utils';
import type { WorkflowState } from '../../workflow-state';

/**
 * Create a success response with optional state updates
 */
export function createSuccessResponse<TState = typeof WorkflowState.State>(
	config: ToolRunnableConfig,
	message: string,
	stateUpdates?: StateUpdater<TState>,
): Command {
	const toolCallId = config.toolCall?.id as string;

	const messages = [
		new ToolMessage({
			content: message,
			tool_call_id: toolCallId,
			name: config.toolCall?.name,
		}),
	];

	const update = { messages };

	if (stateUpdates) {
		Object.assign(update, stateUpdates);
	}

	return new Command({ update });
}

/**
 * Create an error response
 */
export function createErrorResponse(config: ToolRunnableConfig, error: ToolError): Command {
	const toolCallId = config.toolCall?.id as string;

	const messages = [
		new ToolMessage({
			content: `Error: ${error.message}`,
			tool_call_id: toolCallId,
			name: config.toolCall?.name,
		}),
	];

	return new Command({ update: { messages } });
}
