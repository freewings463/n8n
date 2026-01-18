"""
MIGRATION-META:
  source_path: packages/cli/src/chat/utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/chat 的模块。导入/依赖:外部:无；内部:@n8n/db、n8n-workflow；本地:无。导出:getMessage、getLastNodeExecuted、shouldResumeImmediately。关键函数/方法:getMessage、getLastNodeExecuted、shouldResumeImmediately。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Chat feature helpers -> application/services/chat
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/chat/utils.ts -> services/n8n/application/cli/services/chat/utils.py

import type { IExecutionResponse } from '@n8n/db';
import type { INode } from 'n8n-workflow';
import { CHAT_WAIT_USER_REPLY, RESPOND_TO_WEBHOOK_NODE_TYPE } from 'n8n-workflow';

const AI_TOOL = 'ai_tool';

/**
 * Returns the message to be sent of the last executed node
 */
export function getMessage(execution: IExecutionResponse) {
	const lastNodeExecuted = execution.data.resultData.lastNodeExecuted;
	if (typeof lastNodeExecuted !== 'string') return undefined;

	const runIndex = execution.data.resultData.runData[lastNodeExecuted].length - 1;
	const data = execution.data.resultData.runData[lastNodeExecuted][runIndex]?.data;
	const outputs = data?.main ?? data?.[AI_TOOL];

	// Check all main output branches for a message
	if (outputs && Array.isArray(outputs)) {
		for (const branch of outputs) {
			if (branch && Array.isArray(branch) && branch.length > 0 && branch[0].sendMessage) {
				return branch[0].sendMessage;
			}
		}
	}

	return undefined;
}

/**
 * Returns the last node executed
 */
export function getLastNodeExecuted(execution: IExecutionResponse) {
	const lastNodeExecuted = execution.data.resultData.lastNodeExecuted;
	if (typeof lastNodeExecuted !== 'string') return undefined;
	return execution.workflowData?.nodes?.find((node) => node.name === lastNodeExecuted);
}

/**
 * Check if execution should be resumed immediately after receivng a message
 */
export function shouldResumeImmediately(lastNode: INode) {
	if (lastNode?.type === RESPOND_TO_WEBHOOK_NODE_TYPE) {
		return true;
	}

	if (lastNode?.parameters?.[CHAT_WAIT_USER_REPLY] === false) {
		return true;
	}

	const options = lastNode?.parameters?.options as {
		[CHAT_WAIT_USER_REPLY]?: boolean;
	};

	if (options && options[CHAT_WAIT_USER_REPLY] === false) {
		return true;
	}

	return false;
}
