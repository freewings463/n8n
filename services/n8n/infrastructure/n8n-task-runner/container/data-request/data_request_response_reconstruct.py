"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/data-request/data-request-response-reconstruct.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/data-request 的模块。导入/依赖:外部:无；内部:n8n-workflow、@/runner-types；本地:无。导出:DataRequestResponseReconstruct。关键函数/方法:reconstructConnectionInputItems、reconstructExecuteData。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/data-request/data-request-response-reconstruct.ts -> services/n8n/infrastructure/n8n-task-runner/container/data-request/data_request_response_reconstruct.py

import type { IExecuteData, INodeExecutionData, ITaskDataConnections } from 'n8n-workflow';

import type { DataRequestResponse, InputDataChunkDefinition } from '@/runner-types';

/**
 * Reconstructs data from a DataRequestResponse to the initial
 * data structures.
 */
export class DataRequestResponseReconstruct {
	/**
	 * Reconstructs `inputData` from a DataRequestResponse
	 */
	reconstructConnectionInputItems(
		inputData: DataRequestResponse['inputData'],
		chunk?: InputDataChunkDefinition,
	): Array<INodeExecutionData | undefined> {
		const inputItems = inputData?.main?.[0] ?? [];
		if (!chunk) {
			return inputItems;
		}

		// Only a chunk of the input items was requested. We reconstruct
		// the array by filling in the missing items with `undefined`.
		let sparseInputItems: Array<INodeExecutionData | undefined> = [];

		sparseInputItems = sparseInputItems
			.concat(Array.from({ length: chunk.startIndex }))
			.concat(inputItems)
			.concat(Array.from({ length: inputItems.length - chunk.startIndex - chunk.count }));

		return sparseInputItems;
	}

	/**
	 * Reconstruct `executeData` from a DataRequestResponse
	 */
	reconstructExecuteData(
		response: DataRequestResponse,
		inputItems: INodeExecutionData[],
	): IExecuteData {
		const inputData: ITaskDataConnections = {
			...response.inputData,
			main: [inputItems],
		};

		return {
			data: inputData,
			node: response.node,
			source: response.connectionInputSource,
		};
	}
}
