"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/execution-lifecycle-hooks.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine 的执行模块。导入/依赖:外部:无；内部:无；本地:无。导出:ExecutionLifecycleHookHandlers、ExecutionLifecycleHookName、ExecutionLifecycleHooks。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/execution-lifecycle-hooks.ts -> services/n8n/application/core/services/execution_engine/execution_lifecycle_hooks.py

import type {
	IDataObject,
	IExecuteResponsePromiseData,
	INode,
	IRun,
	IRunExecutionData,
	ITaskData,
	ITaskStartedData,
	IWorkflowBase,
	StructuredChunk,
	Workflow,
	WorkflowExecuteMode,
} from 'n8n-workflow';

export type ExecutionLifecycleHookHandlers = {
	nodeExecuteBefore: Array<
		(
			this: ExecutionLifecycleHooks,
			nodeName: string,
			data: ITaskStartedData,
		) => Promise<void> | void
	>;

	nodeExecuteAfter: Array<
		(
			this: ExecutionLifecycleHooks,
			nodeName: string,
			data: ITaskData,
			executionData: IRunExecutionData,
		) => Promise<void> | void
	>;

	workflowExecuteBefore: Array<
		(
			this: ExecutionLifecycleHooks,
			workflow: Workflow,
			data?: IRunExecutionData,
		) => Promise<void> | void
	>;

	workflowExecuteAfter: Array<
		(this: ExecutionLifecycleHooks, data: IRun, newStaticData: IDataObject) => Promise<void> | void
	>;

	/** Used by trigger and webhook nodes to respond back to the request */
	sendResponse: Array<
		(this: ExecutionLifecycleHooks, response: IExecuteResponsePromiseData) => Promise<void> | void
	>;

	/** Used by nodes to send chunks to streaming responses */
	sendChunk: Array<(this: ExecutionLifecycleHooks, chunk: StructuredChunk) => Promise<void> | void>;

	/**
	 * Executed after a node fetches data
	 * - For a webhook node, after the node had been run.
   * - For a http-request node, or any other node that makes http requests that still use the deprecated request* methods, after every successful http request
s	 */
	nodeFetchedData: Array<
		(this: ExecutionLifecycleHooks, workflowId: string, node: INode) => Promise<void> | void
	>;
};

export type ExecutionLifecycleHookName = keyof ExecutionLifecycleHookHandlers;

/**
 * Contains hooks that trigger at specific events in an execution's lifecycle. Every hook has an array of callbacks to run.
 *
 * Common use cases include:
 * - Saving execution progress to database
 * - Pushing execution status updates to the frontend
 * - Recording workflow statistics
 * - Running external hooks for execution events
 * - Error and Cancellation handling and cleanup
 *
 * @example
 * ```typescript
 * const hooks = new ExecutionLifecycleHooks(mode, executionId, workflowData);
 * hooks.add('workflowExecuteAfter, async function(fullRunData) {
 *  await saveToDatabase(executionId, fullRunData);
 *});
 * ```
 */
export class ExecutionLifecycleHooks {
	readonly handlers: ExecutionLifecycleHookHandlers = {
		nodeExecuteAfter: [],
		nodeExecuteBefore: [],
		nodeFetchedData: [],
		sendResponse: [],
		workflowExecuteAfter: [],
		workflowExecuteBefore: [],
		sendChunk: [],
	};

	constructor(
		readonly mode: WorkflowExecuteMode,
		readonly executionId: string,
		readonly workflowData: IWorkflowBase,
	) {}

	addHandler<Hook extends keyof ExecutionLifecycleHookHandlers>(
		hookName: Hook,
		...handlers: Array<ExecutionLifecycleHookHandlers[Hook][number]>
	): void {
		// @ts-expect-error FIX THIS
		this.handlers[hookName].push(...handlers);
	}

	async runHook<
		Hook extends keyof ExecutionLifecycleHookHandlers,
		Params extends unknown[] = Parameters<
			Exclude<ExecutionLifecycleHookHandlers[Hook], undefined>[number]
		>,
	>(hookName: Hook, parameters: Params) {
		const hooks = this.handlers[hookName];
		for (const hookFunction of hooks) {
			const typedHookFunction = hookFunction as unknown as (
				this: ExecutionLifecycleHooks,
				...args: Params
			) => Promise<void>;
			await typedHookFunction.apply(this, parameters);
		}
	}
}
