"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/CustomerIo/EventDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/CustomerIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventOperations、eventFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/CustomerIo/EventDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/CustomerIo/EventDescription.py

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
				description: 'Track a customer event',
				action: 'Track a customer event',
			},
			{
				name: 'Track Anonymous',
				value: 'trackAnonymous',
				description: 'Track an anonymous event',
				action: 'Track an anonymous event',
			},
		],
		default: 'track',
	},
];

export const eventFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   event:track                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Customer ID',
		name: 'customerId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
		description: 'The unique identifier for the customer',
	},
	{
		displayName: 'Event Name',
		name: 'eventName',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
			},
		},
		description: 'Name of the event to track',
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
		displayName: 'Additional Fields',
		name: 'additionalFieldsJson',
		type: 'json',
		typeOptions: {
			alwaysOpenEditWindow: true,
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['track'],
				jsonParameters: [true],
			},
		},
		description:
			'Object of values to set as described <a href="https://customer.io/docs/api-triggered-data-format#basic-data-formatting">here</a>',
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
				jsonParameters: [false],
			},
		},
		options: [
			{
				displayName: 'Custom Attributes',
				name: 'customAttributes',
				type: 'fixedCollection',
				default: {},
				description: 'Custom Properties',
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						displayName: 'Attribute',
						name: 'customAttribute',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								required: true,
								default: '',
								description: 'Attribute name',
								placeholder: 'Price',
							},

							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								required: true,
								default: '',
								description: 'Attribute value',
								placeholder: '25.50',
							},
						],
					},
				],
			},
			{
				displayName: 'Type',
				name: 'type',
				type: 'string',
				default: '',
				description: 'Used to change event type. For Page View events set to "page".',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                   event:track anonymous                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Event Name',
		name: 'eventName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['trackAnonymous'],
			},
		},
		description: 'The unique identifier for the customer',
	},
	{
		displayName: 'JSON Parameters',
		name: 'jsonParameters',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['trackAnonymous'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFieldsJson',
		type: 'json',
		typeOptions: {
			alwaysOpenEditWindow: true,
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['trackAnonymous'],
				jsonParameters: [true],
			},
		},
		description:
			'Object of values to set as described <a href="https://customer.io/docs/api-triggered-data-format#basic-data-formatting">here</a>',
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
				operation: ['trackAnonymous'],
				jsonParameters: [false],
			},
		},
		options: [
			{
				displayName: 'Custom Attributes',
				name: 'customAttributes',
				type: 'fixedCollection',
				default: {},
				description: 'Custom Properties',
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						displayName: 'Attribute',
						name: 'customAttribute',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								required: true,
								default: '',
								description: 'Attribute name',
								placeholder: 'Price',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								required: true,
								default: '',
								description: 'Attribute value',
								placeholder: '25.50',
							},
						],
					},
				],
			},
		],
	},
];
