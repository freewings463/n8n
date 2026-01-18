"""
MIGRATION-META:
  source_path: packages/cli/src/executions/execution.utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/executions 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getWorkflowActiveStatusFromWorkflowData、isManualOrChatExecution。关键函数/方法:getWorkflowActiveStatusFromWorkflowData、isManualOrChatExecution。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution read/write helpers -> application/services/executions
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/executions/execution.utils.ts -> services/n8n/application/cli/services/executions/execution_utils.py

import type { IWorkflowBase } from 'n8n-workflow';

/**
 * Determines the active status of a workflow from workflow data.
 *
 * This function handles backward compatibility:
 * - Newer workflow data uses `activeVersionId` (string = active, null/undefined = inactive)
 * - Older workflow data (before activeVersionId was introduced) falls back to the `active` boolean field
 *
 * @param workflowData - Workflow data
 * @returns true if the workflow should be considered active, false otherwise
 */
export function getWorkflowActiveStatusFromWorkflowData(workflowData: IWorkflowBase): boolean {
	return !!workflowData.activeVersionId || workflowData.active;
}

/**
 * Determines if an execution mode is manual or chat.
 *
 * Manual and chat executions use draft sub-workflows to enable
 * iterating on sub-workflows without requiring them to be published.
 *
 * Note: Test webhooks use 'manual' execution mode, so they also use draft versions.
 * Production webhooks use 'webhook' execution mode and use published versions.
 */
export function isManualOrChatExecution(executionMode?: string): boolean {
	if (!executionMode) return false;
	return ['manual', 'chat'].includes(executionMode);
}
