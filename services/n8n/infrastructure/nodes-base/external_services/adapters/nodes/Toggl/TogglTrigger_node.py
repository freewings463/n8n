"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Toggl/TogglTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Toggl 的节点。导入/依赖:外部:luxon、moment-timezone；内部:n8n-workflow；本地:./GenericFunctions。导出:TogglTrigger。关键函数/方法:poll。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Toggl/TogglTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Toggl/TogglTrigger_node.py

import { DateTime } from 'luxon';
import moment from 'moment-timezone';
import type {
	IPollFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError, NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { togglApiRequest } from './GenericFunctions';

export class TogglTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Toggl Trigger',
		name: 'togglTrigger',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:toggl.png',
		group: ['trigger'],
		version: 1,
		description: 'Starts the workflow when Toggl events occur',
		defaults: {
			name: 'Toggl Trigger',
		},
		credentials: [
			{
				name: 'togglApi',
				required: true,
			},
		],
		polling: true,
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Event',
				name: 'event',
				type: 'options',
				options: [
					{
						name: 'New Time Entry',
						value: 'newTimeEntry',
					},
				],
				required: true,
				default: 'newTimeEntry',
			},
		],
	};

	async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
		const webhookData = this.getWorkflowStaticData('node');
		const event = this.getNodeParameter('event') as string;
		let endpoint: string;

		if (event === 'newTimeEntry') {
			endpoint = '/time_entries';
		} else {
			throw new NodeOperationError(this.getNode(), `The defined event "${event}" is not supported`);
		}

		const qs: IDataObject = {};
		let timeEntries = [];
		qs.start_date = webhookData.lastTimeChecked ?? DateTime.now().toISODate();
		qs.end_date = moment().format();

		try {
			timeEntries = await togglApiRequest.call(this, 'GET', endpoint, {}, qs);
			webhookData.lastTimeChecked = qs.end_date;
		} catch (error) {
			throw new NodeApiError(this.getNode(), error as JsonObject);
		}
		if (Array.isArray(timeEntries) && timeEntries.length !== 0) {
			return [this.helpers.returnJsonArray(timeEntries)];
		}

		return null;
	}
}
