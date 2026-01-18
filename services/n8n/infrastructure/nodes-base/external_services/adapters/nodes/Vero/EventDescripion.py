"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Vero/EventDescripion.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Vero 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventOperations、eventFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Vero/EventDescripion.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Vero/EventDescripion.py

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
				description: 'Track an event for a specific customer',
				action: 'Track an event',
			},
		],
		default: 'track',
	},
];

export const eventFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                event:track                                     */
	/* -------------------------------------------------------------------------- */

	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
		description: 'The unique identifier of the customer',
	},
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
	},
	{
		displayName: 'Event Name',
		name: 'eventName',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
		description: 'The name of the event tracked',
	},
	{
		displayName: 'JSON Parameters',
		name: 'jsonParameters',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
	},
	{
		displayName: 'Data',
		name: 'dataAttributesUi',
		placeholder: 'Add Data',
		description: 'Key value pairs that represent any properties you want to track with this event',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
				jsonParameters: [false],
			},
		},
		options: [
			{
				name: 'dataAttributesValues',
				displayName: 'Data',
				values: [
					{
						displayName: 'Key',
						name: 'key',
						type: 'string',
						default: '',
						description: 'Name of the property to set',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the property to set',
					},
				],
			},
		],
	},
	{
		displayName: 'Extra',
		name: 'extraAttributesUi',
		placeholder: 'Add Extra',
		description:
			'Key value pairs that represent reserved, Vero-specific operators. Refer to the note on “deduplication” below.',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
				jsonParameters: [false],
			},
		},
		options: [
			{
				name: 'extraAttributesValues',
				displayName: 'Extra',
				values: [
					{
						displayName: 'Key',
						name: 'key',
						type: 'string',
						default: '',
						description: 'Name of the property to set',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the property to set',
					},
				],
			},
		],
	},
	{
		displayName: 'Data',
		name: 'dataAttributesJson',
		type: 'json',
		default: '',
		typeOptions: {
			alwaysOpenEditWindow: true,
		},
		description: 'Key value pairs that represent the custom user properties you want to update',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
				jsonParameters: [true],
			},
		},
	},
	{
		displayName: 'Extra',
		name: 'extraAttributesJson',
		type: 'json',
		default: '',
		typeOptions: {
			alwaysOpenEditWindow: true,
		},
		description:
			'Key value pairs that represent reserved, Vero-specific operators. Refer to the note on “deduplication” below.',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
				jsonParameters: [true],
			},
		},
	},
];
