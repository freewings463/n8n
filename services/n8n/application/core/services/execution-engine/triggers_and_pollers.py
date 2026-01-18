"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/triggers-and-pollers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine 的执行模块。导入/依赖:外部:node:assert；内部:@n8n/di、@n8n/errors；本地:./interfaces。导出:TriggersAndPollers。关键函数/方法:runTrigger、resolve、reject、runPoll。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/triggers-and-pollers.ts -> services/n8n/application/core/services/execution-engine/triggers_and_pollers.py

import { Service } from '@n8n/di';
import { ApplicationError } from '@n8n/errors';
import type {
	Workflow,
	INode,
	INodeExecutionData,
	IPollFunctions,
	IWorkflowExecuteAdditionalData,
	WorkflowExecuteMode,
	WorkflowActivateMode,
	ITriggerResponse,
	IDeferredPromise,
	IExecuteResponsePromiseData,
	IRun,
} from 'n8n-workflow';
import assert from 'node:assert';

import type { IGetExecuteTriggerFunctions } from './interfaces';

@Service()
export class TriggersAndPollers {
	/**
	 * Runs the given trigger node so that it can trigger the workflow when the node has data.
	 */
	async runTrigger(
		workflow: Workflow,
		node: INode,
		getTriggerFunctions: IGetExecuteTriggerFunctions,
		additionalData: IWorkflowExecuteAdditionalData,
		mode: WorkflowExecuteMode,
		activation: WorkflowActivateMode,
	): Promise<ITriggerResponse | undefined> {
		const triggerFunctions = getTriggerFunctions(workflow, node, additionalData, mode, activation);

		const nodeType = workflow.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);

		if (!nodeType.trigger) {
			throw new ApplicationError('Node type does not have a trigger function defined', {
				extra: { nodeName: node.name },
				tags: { nodeType: node.type },
			});
		}

		if (mode === 'manual') {
			// In manual mode we do not just start the trigger function we also
			// want to be able to get informed as soon as the first data got emitted
			const triggerResponse = await nodeType.trigger.call(triggerFunctions);

			// Add the manual trigger response which resolves when the first time data got emitted
			triggerResponse!.manualTriggerResponse = new Promise((resolve, reject) => {
				const { hooks } = additionalData;
				assert.ok(hooks, 'Execution lifecycle hooks are not defined');

				triggerFunctions.emit = (
					data: INodeExecutionData[][],
					responsePromise?: IDeferredPromise<IExecuteResponsePromiseData>,
					donePromise?: IDeferredPromise<IRun>,
				) => {
					if (responsePromise) {
						hooks.addHandler('sendResponse', (response) => responsePromise.resolve(response));
					}

					if (donePromise) {
						hooks.addHandler('workflowExecuteAfter', (runData) => donePromise.resolve(runData));
					}

					resolve(data);
				};

				triggerFunctions.emitError = (
					error: Error,
					responsePromise?: IDeferredPromise<IExecuteResponsePromiseData>,
				) => {
					if (responsePromise) {
						hooks.addHandler('sendResponse', () => responsePromise.reject(error));
					}
					reject(error);
				};
			});

			return triggerResponse;
		}
		// In all other modes simply start the trigger
		return await nodeType.trigger.call(triggerFunctions);
	}

	/**
	 * Runs the given poller node so that it can trigger the workflow when the node has data.
	 */
	async runPoll(
		workflow: Workflow,
		node: INode,
		pollFunctions: IPollFunctions,
	): Promise<INodeExecutionData[][] | null> {
		const nodeType = workflow.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);

		if (!nodeType.poll) {
			throw new ApplicationError('Node type does not have a poll function defined', {
				extra: { nodeName: node.name },
				tags: { nodeType: node.type },
			});
		}

		return await nodeType.poll.call(pollFunctions);
	}
}
