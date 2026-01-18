"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/calendar/update.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/calendar/update.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/calendar/update_operation.py

import type { IDataObject, IExecuteFunctions, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { calendarRLC } from '../../descriptions';
import { microsoftApiRequest } from '../../transport';

export const properties: INodeProperties[] = [
	calendarRLC,
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Color',
				name: 'color',
				type: 'options',
				default: 'lightBlue',
				options: [
					{
						name: 'Light Blue',
						value: 'lightBlue',
					},
					{
						name: 'Light Brown',
						value: 'lightBrown',
					},
					{
						name: 'Light Gray',
						value: 'lightGray',
					},
					{
						name: 'Light Green',
						value: 'lightGreen',
					},
					{
						name: 'Light Orange',
						value: 'lightOrange',
					},
					{
						name: 'Light Pink',
						value: 'lightPink',
					},
					{
						name: 'Light Red',
						value: 'lightRed',
					},
					{
						name: 'Light Teal',
						value: 'lightTeal',
					},
					{
						name: 'Light Yellow',
						value: 'lightYellow',
					},
				],
				description: 'Specify the color to distinguish the calendar from the others',
			},
			{
				displayName: 'Default Calendar',
				name: 'isDefaultCalendar',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				placeholder: 'e.g. My Calendar',
				description: 'The name of the calendar',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['calendar'],
		operation: ['update'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, index: number) {
	const updateFields = this.getNodeParameter('updateFields', index);

	const calendarId = this.getNodeParameter('calendarId', index, undefined, {
		extractValue: true,
	}) as string;

	const endpoint = `/calendars/${calendarId}`;

	const body: IDataObject = {
		...updateFields,
	};

	const responseData = await microsoftApiRequest.call(this, 'PATCH', endpoint, body);

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray(responseData as IDataObject),
		{ itemData: { item: index } },
	);

	return executionData;
}
