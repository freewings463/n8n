"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8nTrigger/N8nTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8nTrigger 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:N8nTrigger。关键函数/方法:trigger、events、manualTriggerFunction。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8nTrigger/N8nTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8nTrigger/N8nTrigger_node.py

import type {
	ITriggerFunctions,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

type eventType = 'Instance started' | 'Workflow published' | 'Workflow updated' | undefined;

export class N8nTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'n8n Trigger',
		name: 'n8nTrigger',
		icon: 'file:n8nTrigger.svg',
		group: ['trigger'],
		version: 1,
		description: 'Handle events and perform actions on your n8n instance',
		eventTriggerDescription: '',
		mockManualExecution: true,
		defaults: {
			name: 'n8n Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Events',
				name: 'events',
				type: 'multiOptions',
				required: true,
				default: [],
				description: `Specifies under which conditions an execution should happen:
				<ul>
					<li><b>Published Workflow Updated</b>: Triggers when workflow version is published from a published state (workflow was already published)</li>
					<li><b>Instance Started</b>:  Triggers when this n8n instance is started or re-started</li>
					<li><b>Workflow Published</b>: Triggers when workflow version is published from an unpublished state (workflow was unpublished)</li>
				</ul>`,
				options: [
					{
						name: 'Published Workflow Updated',
						value: 'update',
						description:
							'Triggers when workflow version is published from a published state (workflow was already published)',
					},
					{
						name: 'Instance Started',
						value: 'init',
						description: 'Triggers when this n8n instance is started or re-started',
					},
					{
						name: 'Workflow Published',
						value: 'activate',
						description:
							'Triggers when workflow version is published from an unpublished state (workflow was not published)',
					},
				],
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const events = (this.getNodeParameter('events') as string[]) || [];

		const activationMode = this.getActivationMode();

		if (events.includes(activationMode)) {
			let event: eventType;
			if (activationMode === 'activate') {
				event = 'Workflow published';
			}
			if (activationMode === 'update') {
				event = 'Workflow updated';
			}
			if (activationMode === 'init') {
				event = 'Instance started';
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
