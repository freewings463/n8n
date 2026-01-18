"""
MIGRATION-META:
  source_path: packages/workflow/src/run-execution-data/run-execution-data.v0.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/run-execution-data 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:IRunExecutionDataV0。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/run-execution-data/run-execution-data.v0.ts -> services/n8n/domain/workflow/services/run-execution-data/run_execution_data_v0.py

import type {
	ExecutionError,
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

export interface IRunExecutionDataV0 {
	version?: 0; // Missing version means version 0
	startData?: {
		startNodes?: StartNodeData[];
		destinationNode?: string;
		originalDestinationNode?: string;
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
