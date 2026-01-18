"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/execution-lifecycle/lifecycle-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/execution-lifecycle 的执行模块。导入/依赖:外部:无；内部:@n8n/di；本地:../types。导出:LifecycleHandlerClass、NodeExecuteBeforeContext、NodeExecuteAfterContext、WorkflowExecuteBeforeContext、WorkflowExecuteAfterContext、LifecycleContext、LifecycleEvent、LifecycleMetadata。关键函数/方法:register、getHandlers。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/execution-lifecycle/lifecycle-metadata.ts -> services/n8n/application/n8n-decorators/services/execution-lifecycle/lifecycle_metadata.py

import { Service } from '@n8n/di';
import type {
	IDataObject,
	IRun,
	IRunExecutionData,
	ITaskData,
	ITaskStartedData,
	IWorkflowBase,
	Workflow,
} from 'n8n-workflow';

import type { Class } from '../types';

export type LifecycleHandlerClass = Class<
	Record<string, (ctx: LifecycleContext) => Promise<void> | void>
>;

export type NodeExecuteBeforeContext = {
	type: 'nodeExecuteBefore';
	workflow: IWorkflowBase;
	nodeName: string;
	taskData: ITaskStartedData;
};

export type NodeExecuteAfterContext = {
	type: 'nodeExecuteAfter';
	workflow: IWorkflowBase;
	nodeName: string;
	taskData: ITaskData;
	executionData: IRunExecutionData;
};

export type WorkflowExecuteBeforeContext = {
	type: 'workflowExecuteBefore';
	workflow: IWorkflowBase;
	workflowInstance: Workflow;
	executionData?: IRunExecutionData;
};

export type WorkflowExecuteAfterContext = {
	type: 'workflowExecuteAfter';
	workflow: IWorkflowBase;
	runData: IRun;
	newStaticData: IDataObject;
};

/** Context arg passed to a lifecycle event handler method. */
export type LifecycleContext =
	| NodeExecuteBeforeContext
	| NodeExecuteAfterContext
	| WorkflowExecuteBeforeContext
	| WorkflowExecuteAfterContext;

type LifecycleHandler = {
	/** Class holding the method to call on a lifecycle event. */
	handlerClass: LifecycleHandlerClass;

	/** Name of the method to call on a lifecycle event. */
	methodName: string;

	/** Name of the lifecycle event to listen to. */
	eventName: LifecycleEvent;
};

export type LifecycleEvent = LifecycleContext['type'];

@Service()
export class LifecycleMetadata {
	private readonly handlers: LifecycleHandler[] = [];

	register(handler: LifecycleHandler) {
		this.handlers.push(handler);
	}

	getHandlers(): LifecycleHandler[] {
		return this.handlers;
	}
}
