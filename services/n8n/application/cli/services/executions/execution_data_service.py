"""
MIGRATION-META:
  source_path: packages/cli/src/executions/execution-data.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/executions 的执行服务。导入/依赖:外部:无；内部:@n8n/di；本地:无。导出:ExecutionDataService。关键函数/方法:generateFailedExecutionFromError。用于封装执行业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/executions/execution-data.service.ts -> services/n8n/application/cli/services/executions/execution_data_service.py

import { Service } from '@n8n/di';
import {
	createRunExecutionData,
	type ExecutionError,
	type INode,
	type IRun,
	type WorkflowExecuteMode,
} from 'n8n-workflow';

@Service()
export class ExecutionDataService {
	generateFailedExecutionFromError(
		mode: WorkflowExecuteMode,
		error: ExecutionError,
		node: INode | undefined,
		startTime = Date.now(),
	): IRun {
		const executionError = {
			...error,
			message: error.message,
			stack: error.stack,
		};
		const returnData: IRun = {
			data: createRunExecutionData({
				resultData: {
					error: executionError,
					runData: {},
				},
			}),
			finished: false,
			mode,
			startedAt: new Date(),
			stoppedAt: new Date(),
			status: 'error',
		};

		if (node) {
			returnData.data.startData = {
				destinationNode: {
					nodeName: node.name,
					mode: 'inclusive',
				},
				runNodeFilter: [node.name],
			};
			returnData.data.resultData.lastNodeExecuted = node.name;
			returnData.data.resultData.runData[node.name] = [
				{
					startTime,
					executionIndex: 0,
					executionTime: 0,
					executionStatus: 'error',
					error: executionError,
					source: [],
				},
			];
			returnData.data.executionData = {
				contextData: {},
				metadata: {},
				waitingExecution: {},
				waitingExecutionSource: {},
				nodeExecutionStack: [
					{
						node,
						data: {},
						source: null,
					},
				],
			};
		}
		return returnData;
	}
}
