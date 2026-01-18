"""
MIGRATION-META:
  source_path: packages/cli/src/execution-lifecycle/save-execution-progress.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/execution-lifecycle 的执行模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/db、@n8n/di、n8n-core、n8n-workflow；本地:无。导出:无。关键函数/方法:saveExecutionProgress。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution lifecycle hooks -> application/services/execution_lifecycle
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/execution-lifecycle/save-execution-progress.ts -> services/n8n/application/cli/services/execution_lifecycle/save_execution_progress.py

import { Logger } from '@n8n/backend-common';
import { ExecutionRepository } from '@n8n/db';
import { Container } from '@n8n/di';
import { ErrorReporter } from 'n8n-core';
import { createRunExecutionData, type IRunExecutionData, type ITaskData } from 'n8n-workflow';

export async function saveExecutionProgress(
	workflowId: string,
	executionId: string,
	nodeName: string,
	data: ITaskData,
	executionData: IRunExecutionData,
) {
	const logger = Container.get(Logger);
	const executionRepository = Container.get(ExecutionRepository);
	const errorReporter = Container.get(ErrorReporter);

	try {
		logger.debug(`Save execution progress to database for execution ID ${executionId} `, {
			executionId,
			nodeName,
		});

		const fullExecutionData = await executionRepository.findSingleExecution(executionId, {
			includeData: true,
			unflattenData: true,
		});

		if (!fullExecutionData) {
			// Something went badly wrong if this happens.
			// This check is here mostly to make typescript happy.
			return;
		}

		if (fullExecutionData.finished) {
			// We already received ´workflowExecuteAfter´ webhook, so this is just an async call
			// that was left behind. We skip saving because the other call should have saved everything
			// so this one is safe to ignore
			return;
		}

		fullExecutionData.data ??= createRunExecutionData();

		const { runData } = fullExecutionData.data.resultData;
		(runData[nodeName] ??= []).push(data);

		fullExecutionData.data.executionData = executionData.executionData;

		// Set last executed node so that it may resume on failure
		fullExecutionData.data.resultData.lastNodeExecuted = nodeName;

		// If the execution was canceled, we do not change the status
		// to running, because it is already canceled.
		if (fullExecutionData.status !== 'canceled') {
			fullExecutionData.status = 'running';
		}

		await executionRepository.updateExistingExecution(executionId, fullExecutionData);
	} catch (e) {
		const error = e instanceof Error ? e : new Error(`${e}`);

		errorReporter.error(error);
		// TODO: Improve in the future!
		// Errors here might happen because of database access
		// For busy machines, we may get "Database is locked" errors.

		// We do this to prevent crashes and executions ending in `unknown` state.
		logger.error(
			`Failed saving execution progress to database for execution ID ${executionId} (hookFunctionsSaveProgress, nodeExecuteAfter)`,
			{ error, executionId, workflowId },
		);
	}
}
