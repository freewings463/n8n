"""
MIGRATION-META:
  source_path: packages/cli/src/execution-lifecycle/to-save-settings.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/execution-lifecycle 的执行模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、n8n-workflow；本地:无。导出:ExecutionSaveSettings、toSaveSettings。关键函数/方法:toSaveSettings。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution lifecycle hooks -> application/services/execution_lifecycle
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/execution-lifecycle/to-save-settings.ts -> services/n8n/application/cli/services/execution_lifecycle/to_save_settings.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';
import type { IWorkflowSettings } from 'n8n-workflow';

export type ExecutionSaveSettings = {
	error: boolean | 'all' | 'none';
	success: boolean | 'all' | 'none';
	manual: boolean;
	progress: boolean;
};

/**
 * Return whether a workflow execution is configured to be saved or not:
 *
 * - `error`: Whether to save failed executions in production.
 * - `success`: Whether to successful executions in production.
 * - `manual`: Whether to save successful or failed manual executions.
 * - `progress`: Whether to save execution progress, i.e. after each node's execution.
 */
export function toSaveSettings(
	workflowSettings: IWorkflowSettings | null = {},
): ExecutionSaveSettings {
	const DEFAULTS = {
		ERROR: Container.get(GlobalConfig).executions.saveDataOnError,
		SUCCESS: Container.get(GlobalConfig).executions.saveDataOnSuccess,
		MANUAL: Container.get(GlobalConfig).executions.saveDataManualExecutions,
		PROGRESS: Container.get(GlobalConfig).executions.saveExecutionProgress,
	};

	const {
		saveDataErrorExecution = DEFAULTS.ERROR,
		saveDataSuccessExecution = DEFAULTS.SUCCESS,
		saveManualExecutions = DEFAULTS.MANUAL,
		saveExecutionProgress = DEFAULTS.PROGRESS,
	} = workflowSettings ?? {};

	return {
		error: saveDataErrorExecution === 'DEFAULT' ? DEFAULTS.ERROR : saveDataErrorExecution === 'all',
		success:
			saveDataSuccessExecution === 'DEFAULT'
				? DEFAULTS.SUCCESS
				: saveDataSuccessExecution === 'all',
		manual: saveManualExecutions === 'DEFAULT' ? DEFAULTS.MANUAL : saveManualExecutions,
		progress: saveExecutionProgress === 'DEFAULT' ? DEFAULTS.PROGRESS : saveExecutionProgress,
	};
}
