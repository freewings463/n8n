"""
MIGRATION-META:
  source_path: packages/cli/src/execution-lifecycle/restore-binary-data-id.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/execution-lifecycle 的执行模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di、n8n-core、n8n-workflow；本地:无。导出:无。关键函数/方法:restoreBinaryDataId。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution lifecycle hooks -> application/services/execution_lifecycle
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/execution-lifecycle/restore-binary-data-id.ts -> services/n8n/application/cli/services/execution_lifecycle/restore_binary_data_id.py

import { Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import type { BinaryData } from 'n8n-core';
import { BinaryDataConfig, BinaryDataService } from 'n8n-core';
import type { IRun, WorkflowExecuteMode } from 'n8n-workflow';

/**
 * Whenever the execution ID is not available to the binary data service at the
 * time of writing a binary data file, its name is missing the execution ID.
 * This function restores the ID in the file name and run data reference.
 *
 * This edge case can happen only for a Webhook node that accepts binary data,
 * when the binary data manager is set to persist this binary data.
 *
 * ```txt
 * filesystem-v2:workflows/123/executions/temp/binary_data/69055-83c4-4493-876a-9092c4708b9b ->
 * filesystem-v2:workflows/123/executions/390/binary_data/69055-83c4-4493-876a-9092c4708b9b
 *
 * s3:workflows/123/executions/temp/binary_data/69055-83c4-4493-876a-9092c4708b9b ->
 * s3:workflows/123/executions/390/binary_data/69055-83c4-4493-876a-9092c4708b9b
 * ```
 */
export async function restoreBinaryDataId(
	run: IRun,
	executionId: string,
	workflowExecutionMode: WorkflowExecuteMode,
) {
	if (workflowExecutionMode !== 'webhook' || Container.get(BinaryDataConfig).mode === 'default') {
		return;
	}

	try {
		const { runData } = run.data.resultData;

		const promises = Object.keys(runData).map(async (nodeName) => {
			const binaryDataId = runData[nodeName]?.[0]?.data?.main?.[0]?.[0]?.binary?.data?.id;

			if (!binaryDataId) return;

			const [mode, fileId] = binaryDataId.split(':') as [BinaryData.StoredMode, string];

			const isMissingExecutionId = fileId.includes('/temp/');

			if (!isMissingExecutionId) return;

			const correctFileId = fileId.replace('temp', executionId);

			await Container.get(BinaryDataService).rename(fileId, correctFileId);

			const correctBinaryDataId = `${mode}:${correctFileId}`;

			// @ts-expect-error Validated at the top
			run.data.resultData.runData[nodeName][0].data.main[0][0].binary.data.id = correctBinaryDataId;
		});

		await Promise.all(promises);
	} catch (e) {
		const error = e instanceof Error ? e : new Error(`${e}`);
		const logger = Container.get(Logger);

		if (typeof error.message === 'string' && error.message.includes('ENOENT')) {
			logger.warn('Failed to restore binary data ID - No such file or dir', {
				executionId,
				error,
			});
			return;
		}

		logger.error('Failed to restore binary data ID - Unknown error', { executionId, error });
	}
}
