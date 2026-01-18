"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cron/Cron.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cron 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Cron。关键函数/方法:trigger、expressions、executeTrigger。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cron/Cron.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cron/Cron_node.py

import type {
	ITriggerFunctions,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
	TriggerTime,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeHelpers, toCronExpression } from 'n8n-workflow';

export class Cron implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Cron',
		name: 'cron',
		icon: 'fa:clock',
		group: ['trigger', 'schedule'],
		version: 1,
		hidden: true,
		description: 'Triggers the workflow at a specific time',
		eventTriggerDescription: '',
		activationMessage:
			'Your cron trigger will now trigger executions on the schedule you have defined.',
		defaults: {
			name: 'Cron',
			color: '#29a568',
		},

		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName:
					"This workflow will run on the schedule you define here once you publish it.<br><br>For testing, you can also trigger it manually: by going back to the canvas and clicking 'execute workflow'",
				name: 'notice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Trigger Times',
				name: 'triggerTimes',
				type: 'fixedCollection',
				typeOptions: {
					multipleValues: true,
					multipleValueButtonText: 'Add Time',
				},
				default: {},
				description: 'Triggers for the workflow',
				placeholder: 'Add Cron Time',
				options: NodeHelpers.cronNodeOptions,
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const triggerTimes = this.getNodeParameter('triggerTimes') as unknown as {
			item: TriggerTime[];
		};

		// Get all the trigger times
		const expressions = (triggerTimes.item || []).map(toCronExpression);

		// The trigger function to execute when the cron-time got reached
		// or when manually triggered
		const executeTrigger = () => {
			this.emit([this.helpers.returnJsonArray([{}])]);
		};

		// Register the cron-jobs
		expressions.forEach((expression) => this.helpers.registerCron({ expression }, executeTrigger));

		return {
			manualTriggerFunction: async () => executeTrigger(),
		};
	}
}
