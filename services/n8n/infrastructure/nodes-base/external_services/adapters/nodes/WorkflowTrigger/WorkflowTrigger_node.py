"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WorkflowTrigger/WorkflowTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WorkflowTrigger 的工作流节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:WorkflowTrigger。关键函数/方法:trigger、manualTriggerFunction。用于实现 n8n 工作流节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WorkflowTrigger/WorkflowTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WorkflowTrigger/WorkflowTrigger_node.py

import type {
	ITriggerFunctions,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

type eventType = 'Workflow activated' | 'Workflow updated' | undefined;
type activationType = 'activate' | 'update';

export class WorkflowTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Workflow Trigger',
		hidden: true,
		name: 'workflowTrigger',
		icon: 'fa:network-wired',
		iconColor: 'orange-red',
		group: ['trigger'],
		version: 1,
		description: 'Triggers based on various lifecycle events, like when a workflow is activated',
		eventTriggerDescription: '',
		mockManualExecution: true,
		activationMessage: 'Your workflow will now trigger executions on the event you have defined.',
		defaults: {
			name: 'Workflow Trigger',
			color: '#ff6d5a',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName:
					"This node is deprecated and would not be updated in the future. Please use 'n8n Trigger' node instead.",
				name: 'oldVersionNotice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Events',
				name: 'events',
				type: 'multiOptions',
				required: true,
				default: [],
				description: `Specifies under which conditions an execution should happen:
					<ul>
						<li><b>Active Workflow Updated</b>: Triggers when this workflow is updated</li>
						<li><b>Workflow Activated</b>: Triggers when this workflow is activated</li>
					</ul>`,
				options: [
					{
						name: 'Active Workflow Updated',
						value: 'update',
						description: 'Triggers when this workflow is updated',
					},
					{
						name: 'Workflow Activated',
						value: 'activate',
						description: 'Triggers when this workflow is activated',
					},
				],
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const events = this.getNodeParameter('events', []) as activationType[];

		const activationMode = this.getActivationMode() as activationType;

		if (events.includes(activationMode)) {
			let event: eventType;
			if (activationMode === 'activate') {
				event = 'Workflow activated';
			}
			if (activationMode === 'update') {
				event = 'Workflow updated';
			}
			this.emit([
				this.helpers.returnJsonArray([
					{ event, timestamp: new Date().toISOString(), workflow_id: this.getWorkflow().id },
				]),
			]);
		}

		const manualTriggerFunction = async () => {
			this.emit([
				this.helpers.returnJsonArray([
					{
						event: 'Manual execution',
						timestamp: new Date().toISOString(),
						workflow_id: this.getWorkflow().id,
					},
				]),
			]);
		};

		return {
			manualTriggerFunction,
		};
	}
}
