"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ErrorTrigger/ErrorTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ErrorTrigger 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ErrorTrigger。关键函数/方法:execute、trigger。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ErrorTrigger/ErrorTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ErrorTrigger/ErrorTrigger_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	ITriggerFunctions,
	ITriggerResponse,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

export class ErrorTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Error Trigger',
		name: 'errorTrigger',
		icon: 'fa:bug',
		iconColor: 'blue',
		group: ['trigger'],
		version: 1,
		description: 'Triggers the workflow when another workflow has an error',
		eventTriggerDescription: '',
		mockManualExecution: true,
		maxNodes: 1,
		defaults: {
			name: 'Error Trigger',
			color: '#0000FF',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName:
					'This node will trigger when there is an error in another workflow, as long as that workflow is set up to do so. <a href="https://docs.n8n.io/integrations/core-nodes/n8n-nodes-base.errortrigger" target="_blank">More info</a>',
				name: 'notice',
				type: 'notice',
				default: '',
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		// ErrorTrigger is triggered by n8n's error handling system
		// No setup or teardown is required, as the triggering is handled externally
		return {};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();

		const mode = this.getMode();

		if (
			mode === 'manual' &&
			items.length === 1 &&
			Object.keys(items[0].json).length === 0 &&
			items[0].binary === undefined
		) {
			// If we are in manual mode and no input data got provided we return
			// example data to allow to develope and test errorWorkflows easily

			const restApiUrl = this.getRestApiUrl();

			const urlParts = restApiUrl.split('/');
			urlParts.pop();
			urlParts.push('execution');

			const id = 231;

			items[0].json = {
				execution: {
					id,
					url: `${urlParts.join('/')}/workflow/1/${id}`,
					retryOf: '34',
					error: {
						message: 'Example Error Message',
						stack: 'Stacktrace',
					},
					lastNodeExecuted: 'Node With Error',
					mode: 'manual',
				},
				workflow: {
					id: '1',
					name: 'Example Workflow',
				},
			};
		}

		return [items];
	}
}
