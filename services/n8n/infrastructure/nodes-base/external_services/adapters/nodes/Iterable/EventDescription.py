"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Iterable/EventDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Iterable 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventOperations、eventFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Iterable/EventDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Iterable/EventDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const eventOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['event'],
			},
		},
		options: [
			{
				name: 'Track',
				value: 'track',
				description: 'Record the actions a user perform',
				action: 'Track an event',
			},
		],
		default: 'track',
	},
];

export const eventFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                event:track                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
		description: 'The name of the event to track',
		default: '',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
		options: [
			{
				displayName: 'Campaign ID',
				name: 'campaignId',
				type: 'string',
				default: '',
				description: 'Campaign tied to conversion',
			},
			{
				displayName: 'Created At',
				name: 'createdAt',
				type: 'dateTime',
				default: '',
				description: 'Time event happened',
			},
			{
				displayName: 'Data Fields',
				name: 'dataFieldsUi',
				type: 'fixedCollection',
				default: {},
				placeholder: 'Add Data Field',
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						name: 'dataFieldValues',
						displayName: 'Data Field',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								default: '',
								description: 'The end event specified key of the event defined data',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								default: '',
								description: 'The end event specified value of the event defined data',
							},
						],
					},
				],
			},
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
				description:
					'Either email or userId must be passed in to identify the user. If both are passed in, email takes precedence.',
			},
			{
				displayName: 'ID',
				name: 'id',
				type: 'string',
				default: '',
				description:
					'Optional event ID. If an event exists with that ID, the event will be updated. If none is specified, a new ID will automatically be generated and returned.',
			},
			{
				displayName: 'Template ID',
				name: 'templateId',
				type: 'string',
				default: '',
			},
			{
				displayName: 'User ID',
				name: 'userId',
				type: 'string',
				default: '',
				// eslint-disable-next-line n8n-nodes-base/node-param-description-lowercase-first-char
				description: 'userId that was passed into the updateUser call',
			},
		],
	},
];
