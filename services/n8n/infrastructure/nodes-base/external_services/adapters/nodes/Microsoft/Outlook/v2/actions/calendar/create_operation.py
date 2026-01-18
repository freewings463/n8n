"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/calendar/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../transport。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/calendar/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/calendar/create_operation.py

import type { IDataObject, IExecuteFunctions, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { microsoftApiRequest } from '../../transport';

export const properties: INodeProperties[] = [
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		required: true,
		description: 'The name of the calendar to create',
		placeholder: 'e.g. My Calendar',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
				displayName: 'Calendar Group',
				name: 'calendarGroup',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getCalendarGroups',
				},
				default: [],
				description:
					'If set, the calendar will be created in the specified calendar group. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
			},
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
		],
	},
];

const displayOptions = {
	show: {
		resource: ['calendar'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, index: number) {
	const additionalFields = this.getNodeParameter('additionalFields', index);
	const name = this.getNodeParameter('name', index) as string;

	let endpoint = '/calendars';

	if (additionalFields.calendarGroup) {
		endpoint = `/calendarGroups/${additionalFields.calendarGroup}/calendars`;
		delete additionalFields.calendarGroup;
	}

	const body: IDataObject = {
		name,
		...additionalFields,
	};

	const responseData = await microsoftApiRequest.call(this, 'POST', endpoint, body);

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray(responseData as IDataObject),
		{ itemData: { item: index } },
	);

	return executionData;
}
