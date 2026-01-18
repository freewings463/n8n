"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/CustomerIo/CustomerDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/CustomerIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:customerOperations、customerFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/CustomerIo/CustomerDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/CustomerIo/CustomerDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const customerOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['customer'],
			},
		},
		options: [
			{
				name: 'Create or Update',
				value: 'upsert',
				description:
					'Create a new customer, or update the current one if it already exists (upsert)',
				action: 'Create or update a customer',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a customer',
				action: 'Delete a customer',
			},
		],
		default: 'upsert',
	},
];

export const customerFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   customer:delete			            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['delete'],
			},
		},
		description: 'The unique identifier for the customer',
	},

	/* -------------------------------------------------------------------------- */
	/*                                   customer:upsert			              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['upsert'],
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
				resource: ['customer'],
				operation: ['upsert'],
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
				resource: ['customer'],
				operation: ['upsert'],
				jsonParameters: [true],
			},
		},
		description:
			'Object of values to set as described <a href="https://github.com/agilecrm/rest-api#1-companys---companies-api">here</a>',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['upsert'],
				jsonParameters: [false],
			},
		},
		options: [
			{
				displayName: 'Custom Properties',
				name: 'customProperties',
				type: 'fixedCollection',
				default: {},
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						displayName: 'Property',
						name: 'customProperty',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								required: true,
								default: '',
								description: 'Property name',
								placeholder: 'Plan',
							},

							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								required: true,
								default: '',
								description: 'Property value',
								placeholder: 'Basic',
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
				description: 'The email address of the user',
			},
			{
				displayName: 'Created At',
				name: 'createdAt',
				type: 'dateTime',
				default: '',
				description: 'The UNIX timestamp from when the user was created',
			},
		],
	},
];
