"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ICalendar/ICalendar.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ICalendar 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./createEvent.operation。导出:ICalendar。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ICalendar/ICalendar.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ICalendar/ICalendar_node.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import * as createEvent from './createEvent.operation';

export class ICalendar implements INodeType {
	description: INodeTypeDescription = {
		hidden: true,
		displayName: 'iCalendar',
		name: 'iCal',
		icon: 'fa:calendar',
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"]}}',
		description: 'Create iCalendar file',
		defaults: {
			name: 'iCalendar',
			color: '#408000',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Create Event File',
						value: 'createEventFile',
					},
				],
				default: 'createEventFile',
			},
			...createEvent.description,
		],
	};

	async execute(this: IExecuteFunctions) {
		const items = this.getInputData();
		const operation = this.getNodeParameter('operation', 0);

		let returnData: INodeExecutionData[] = [];

		if (operation === 'createEventFile') {
			returnData = await createEvent.execute.call(this, items);
		}

		return [returnData];
	}
}
