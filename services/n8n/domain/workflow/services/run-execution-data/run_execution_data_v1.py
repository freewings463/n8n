"""
MIGRATION-META:
  source_path: packages/workflow/src/run-execution-data/run-execution-data.v1.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/run-execution-data 的工作流模块。导入/依赖:外部:无；内部:无；本地:./run-execution-data.v0。导出:IRunExecutionDataV1、runExecutionDataV0ToV1。关键函数/方法:runExecutionDataV0ToV1。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/run-execution-data/run-execution-data.v1.ts -> services/n8n/domain/workflow/services/run-execution-data/run_execution_data_v1.py

import type {
	ExecutionError,
	IDestinationNode,
	IExecuteContextData,
	IExecuteData,
	IExecutionContext,
	IPinData,
	IRunData,
	ITaskMetadata,
	IWaitingForExecution,
	IWaitingForExecutionSource,
	IWorkflowExecutionDataProcess,
	RelatedExecution,
	StartNodeData,
} from '..';
import type { IRunExecutionDataV0 } from './run-execution-data.v0';

// DIFF: switches startData.destinationNode to a structured object, rather than just the name of the string.
export interface IRunExecutionDataV1 {
	version: 1;
	startData?: {
		startNodes?: StartNodeData[];
		destinationNode?: IDestinationNode;
		originalDestinationNode?: IDestinationNode;
		runNodeFilter?: string[];
	};
	resultData: {
		error?: ExecutionError;
		runData: IRunData;
		pinData?: IPinData;
		lastNodeExecuted?: string;
		metadata?: Record<string, string>;
	};
	executionData?: {
		contextData: IExecuteContextData;
		runtimeData?: IExecutionContext;
		nodeExecutionStack: IExecuteData[];
		metadata: {
			// node-name: metadata by runIndex
			[key: string]: ITaskMetadata[];
		};
		waitingExecution: IWaitingForExecution;
		waitingExecutionSource: IWaitingForExecutionSource | null;
	};
	parentExecution?: RelatedExecution;
	/**
	 * This is used to prevent breaking change
	 * for waiting executions started before signature validation was added
	 */
	validateSignature?: boolean;
	waitTill?: Date;
	pushRef?: string;

	/** Data needed for a worker to run a manual execution. */
	manualData?: Pick<
		IWorkflowExecutionDataProcess,
		'dirtyNodeNames' | 'triggerToStartFrom' | 'userId'
	>;
}

export function runExecutionDataV0ToV1(data: IRunExecutionDataV0): IRunExecutionDataV1 {
	const destinationNodeV0 = data.startData?.destinationNode;
	const originalDestinationNodeV0 = data.startData?.originalDestinationNode;

	return {
		...data,
		version: 1,
		startData: {
			...data.startData,
			destinationNode: destinationNodeV0
				? {
						nodeName: destinationNodeV0,
						mode: 'inclusive',
					}
				: undefined,
			originalDestinationNode: originalDestinationNodeV0
				? {
						nodeName: originalDestinationNodeV0,
						mode: 'inclusive',
					}
				: undefined,
		},
	};
}
