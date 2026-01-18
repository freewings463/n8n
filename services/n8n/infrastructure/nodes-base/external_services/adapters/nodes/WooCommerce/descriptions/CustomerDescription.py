"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WooCommerce/descriptions/CustomerDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WooCommerce/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./shared。导出:customerOperations、customerFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WooCommerce/descriptions/CustomerDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WooCommerce/descriptions/CustomerDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { customerCreateFields, customerUpdateFields } from './shared';

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
				name: 'Create',
				value: 'create',
				description: 'Create a customer',
				action: 'Create a customer',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a customer',
				action: 'Delete a customer',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a customer',
				action: 'Get a customer',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many customers',
				action: 'Get many customers',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a customer',
				action: 'Update a customer',
			},
		],
		default: 'create',
	},
];

export const customerFields: INodeProperties[] = [
	// ----------------------------------------
	//             customer: create
	// ----------------------------------------
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['create'],
			},
		},
	},
	customerCreateFields,

	// ----------------------------------------
	//             customer: delete
	// ----------------------------------------
	{
		displayName: 'Customer ID',
		name: 'customerId',
		description: 'ID of the customer to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//              customer: get
	// ----------------------------------------
	{
		displayName: 'Customer ID',
		name: 'customerId',
		description: 'ID of the customer to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//             customer: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
				description: 'Email address to filter customers by',
			},
			{
				displayName: 'Sort Order',
				name: 'order',
				description: 'Order to sort customers in',
				type: 'options',
				options: [
					{
						name: 'Ascending',
						value: 'asc',
					},
					{
						name: 'Descending',
						value: 'desc',
					},
				],
				default: 'asc',
			},
			{
				displayName: 'Order By',
				name: 'orderby',
				description: 'Field to sort customers by',
				type: 'options',
				options: [
					{
						name: 'ID',
						value: 'id',
					},
					{
						name: 'Include',
						value: 'include',
					},
					{
						name: 'Name',
						value: 'name',
					},
					{
						name: 'Registered Date',
						value: 'registered_date',
					},
				],
				default: 'id',
			},
		],
	},

	// ----------------------------------------
	//             customer: update
	// ----------------------------------------
	{
		displayName: 'Customer ID',
		name: 'customerId',
		description: 'ID of the customer to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['customer'],
				operation: ['update'],
			},
		},
	},
	customerUpdateFields,
];
