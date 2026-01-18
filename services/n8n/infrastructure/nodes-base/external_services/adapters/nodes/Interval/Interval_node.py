"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Interval/Interval.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Interval 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Interval。关键函数/方法:trigger、executeTrigger、closeFunction、clearInterval、manualTriggerFunction。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Interval/Interval.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Interval/Interval_node.py

import type {
	ITriggerFunctions,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

export class Interval implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Interval',
		name: 'interval',
		icon: 'fa:hourglass',
		group: ['trigger', 'schedule'],
		version: 1,
		hidden: true,
		description: 'Triggers the workflow in a given interval',
		eventTriggerDescription: '',
		activationMessage:
			'Your interval trigger will now trigger executions on the schedule you have defined.',
		defaults: {
			name: 'Interval',
			color: '#00FF00',
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
				displayName: 'Interval',
				name: 'interval',
				type: 'number',
				typeOptions: {
					minValue: 1,
				},
				default: 1,
				description: 'Interval value',
			},
			{
				displayName: 'Unit',
				name: 'unit',
				type: 'options',
				options: [
					{
						name: 'Seconds',
						value: 'seconds',
					},
					{
						name: 'Minutes',
						value: 'minutes',
					},
					{
						name: 'Hours',
						value: 'hours',
					},
				],
				default: 'seconds',
				description: 'Unit of the interval value',
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const interval = this.getNodeParameter('interval') as number;
		const unit = this.getNodeParameter('unit') as string;

		if (interval <= 0) {
			throw new NodeOperationError(
				this.getNode(),
				'The interval has to be set to at least 1 or higher!',
			);
		}

		let intervalValue = interval;
		if (unit === 'minutes') {
			intervalValue *= 60;
		}
		if (unit === 'hours') {
			intervalValue *= 60 * 60;
		}

		const executeTrigger = () => {
			this.emit([this.helpers.returnJsonArray([{}])]);
		};

		intervalValue *= 1000;

		// Reference: https://nodejs.org/api/timers.html#timers_setinterval_callback_delay_args
		if (intervalValue > 2147483647) {
			throw new NodeOperationError(this.getNode(), 'The interval value is too large.');
		}

		const intervalObj = setInterval(executeTrigger, intervalValue);

		async function closeFunction() {
			clearInterval(intervalObj);
		}

		async function manualTriggerFunction() {
			executeTrigger();
		}

		return {
			closeFunction,
			manualTriggerFunction,
		};
	}
}
