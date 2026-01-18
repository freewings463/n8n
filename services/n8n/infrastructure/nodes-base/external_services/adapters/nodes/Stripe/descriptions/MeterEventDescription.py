"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Stripe/descriptions/MeterEventDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Stripe/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:meterEventOperations、meterEventFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Stripe/descriptions/MeterEventDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Stripe/descriptions/MeterEventDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const meterEventOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'create',
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a meter event',
				action: 'Create a meter event',
			},
		],
		displayOptions: {
			show: {
				resource: ['meterEvent'],
			},
		},
	},
];

export const meterEventFields: INodeProperties[] = [
	// ----------------------------------
	//       meterEvent: create
	// ----------------------------------
	{
		displayName: 'Event Name',
		name: 'eventName',
		type: 'string',
		required: true,
		default: '',
		description: 'The name of the meter event. Corresponds with the event_name field on a meter.',
		displayOptions: {
			show: {
				resource: ['meterEvent'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Customer ID',
		name: 'customerId',
		type: 'string',
		required: true,
		default: '',
		description: 'The Stripe customer ID associated with this meter event',
		displayOptions: {
			show: {
				resource: ['meterEvent'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Value',
		name: 'value',
		type: 'number',
		required: true,
		default: 1,
		description: 'The value of the meter event. Must be an integer. Can be positive or negative.',
		displayOptions: {
			show: {
				resource: ['meterEvent'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['meterEvent'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Identifier',
				name: 'identifier',
				type: 'string',
				default: '',
				description:
					'A unique identifier for the event. If not provided, one will be generated. Uniqueness is enforced within a rolling 24 hour window.',
			},
			{
				displayName: 'Timestamp',
				name: 'timestamp',
				type: 'dateTime',
				default: '',
				description:
					'The time of the event. Measured in seconds since the Unix epoch. Must be within the past 35 calendar days or up to 5 minutes in the future. Defaults to current time if not specified.',
			},
			{
				displayName: 'Custom Payload Properties',
				name: 'customPayload',
				type: 'fixedCollection',
				default: {},
				placeholder: 'Add Custom Property',
				description:
					'Additional custom properties to include in the event payload. Use this for custom meter configurations with non-default payload keys.',
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						displayName: 'Properties',
						name: 'properties',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								default: '',
								description: 'The property key',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								default: '',
								description: 'The property value',
							},
						],
					},
				],
			},
		],
	},
];
