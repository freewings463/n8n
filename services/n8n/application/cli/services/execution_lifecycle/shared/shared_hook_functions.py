"""
MIGRATION-META:
  source_path: packages/cli/src/execution-lifecycle/shared/shared-hook-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/execution-lifecycle/shared 的执行模块。导入/依赖:外部:lodash/pick；内部:@n8n/backend-common、@n8n/db、@n8n/di、n8n-workflow、@/interfaces、@/services/execution-metadata.service 等1项；本地:无。导出:determineFinalExecutionStatus、prepareExecutionDataForDbUpdate。关键函数/方法:determineFinalExecutionStatus、prepareExecutionDataForDbUpdate、updateExistingExecutionMetadata、updateExistingExecution。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution lifecycle hooks -> application/services/execution_lifecycle
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/execution-lifecycle/shared/shared-hook-functions.ts -> services/n8n/application/cli/services/execution_lifecycle/shared/shared_hook_functions.py

import { Logger } from '@n8n/backend-common';
import type { IExecutionDb } from '@n8n/db';
import { ExecutionRepository } from '@n8n/db';
import { Container } from '@n8n/di';
import pick from 'lodash/pick';
import { ensureError, type ExecutionStatus, type IRun, type IWorkflowBase } from 'n8n-workflow';

import type { UpdateExecutionPayload } from '@/interfaces';
import { ExecutionMetadataService } from '@/services/execution-metadata.service';
import { isWorkflowIdValid } from '@/utils';

export function determineFinalExecutionStatus(runData: IRun): ExecutionStatus {
	const workflowHasCrashed = runData.status === 'crashed';
	const workflowWasCanceled = runData.status === 'canceled';
	const workflowHasFailed = runData.status === 'error';
	const workflowDidSucceed =
		!runData.data.resultData?.error &&
		!workflowHasCrashed &&
		!workflowWasCanceled &&
		!workflowHasFailed;
	let workflowStatusFinal: ExecutionStatus = workflowDidSucceed ? 'success' : 'error';
	if (workflowHasCrashed) workflowStatusFinal = 'crashed';
	if (workflowWasCanceled) workflowStatusFinal = 'canceled';
	if (runData.waitTill) workflowStatusFinal = 'waiting';
	return workflowStatusFinal;
}

export function prepareExecutionDataForDbUpdate(parameters: {
	runData: IRun;
	workflowData: IWorkflowBase;
	workflowStatusFinal: ExecutionStatus;
	retryOf?: string;
}) {
	const { runData, workflowData, workflowStatusFinal, retryOf } = parameters;
	// Although it is treated as IWorkflowBase here, it's being instantiated elsewhere with properties that may be sensitive
	// As a result, we should create an IWorkflowBase object with only the data we want to save in it.
	const pristineWorkflowData: IWorkflowBase = pick(workflowData, [
		'id',
		'name',
		'active',
		'activeVersionId',
		'isArchived',
		'createdAt',
		'updatedAt',
		'nodes',
		'connections',
		'settings',
		'staticData',
		'pinData',
	]);

	const fullExecutionData: UpdateExecutionPayload = {
		data: runData.data,
		mode: runData.mode,
		finished: runData.finished ? runData.finished : false,
		startedAt: runData.startedAt,
		stoppedAt: runData.stoppedAt,
		workflowData: pristineWorkflowData,
		waitTill: runData.waitTill,
		status: workflowStatusFinal,
		workflowId: pristineWorkflowData.id,
	};

	if (retryOf !== undefined) {
		fullExecutionData.retryOf = retryOf.toString();
	}

	const workflowId = workflowData.id;
	if (isWorkflowIdValid(workflowId)) {
		fullExecutionData.workflowId = workflowId;
	}

	return fullExecutionData;
}

export async function updateExistingExecutionMetadata(
	executionId: string,
	metadata?: Record<string, string>,
) {
	const logger = Container.get(Logger);

	try {
		if (metadata && Object.keys(metadata).length > 0) {
			await Container.get(ExecutionMetadataService).save(executionId, metadata);
		}
	} catch (e) {
		const error = ensureError(e);
		logger.error(`Failed to save metadata for execution ID ${executionId}`, { error });
	}
}

export async function updateExistingExecution(parameters: {
	executionId: string;
	workflowId: string;
	executionData: Partial<IExecutionDb>;
}) {
	const logger = Container.get(Logger);
	const { executionId, workflowId, executionData } = parameters;
	// Leave log message before flatten as that operation increased memory usage a lot and the chance of a crash is highest here
	logger.debug(`Save execution data to database for execution ID ${executionId}`, {
		executionId,
		workflowId,
		finished: executionData.finished,
		stoppedAt: executionData.stoppedAt,
	});

	await Container.get(ExecutionRepository).updateExistingExecution(executionId, executionData);

	if (executionData.finished === true && executionData.retryOf !== undefined) {
		await Container.get(ExecutionRepository).updateExistingExecution(executionData.retryOf, {
			retrySuccessId: executionId,
		});
	}
}
