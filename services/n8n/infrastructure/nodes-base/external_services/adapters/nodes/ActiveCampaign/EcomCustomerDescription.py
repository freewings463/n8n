"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActiveCampaign/EcomCustomerDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActiveCampaign 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:ecomCustomerOperations、ecomCustomerFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActiveCampaign/EcomCustomerDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActiveCampaign/EcomCustomerDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { activeCampaignDefaultGetAllProperties } from './GenericFunctions';

export const ecomCustomerOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['ecommerceCustomer'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a E-commerce Customer',
				action: 'Create an e-commerce customer',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a E-commerce Customer',
				action: 'Delete an e-commerce customer',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get data of a E-commerce Customer',
				action: 'Get an e-commerce customer',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get data of many E-commerce Customers',
				action: 'Get many e-commerce customers',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a E-commerce Customer',
				action: 'Update an e-commerce customer',
			},
		],
		default: 'create',
	},
];

export const ecomCustomerFields: INodeProperties[] = [
	// ----------------------------------
	//         ecommerceCustomer:create
	// ----------------------------------
	{
		displayName: 'Service ID',
		name: 'connectionid',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['ecommerceCustomer'],
			},
		},
		description: 'The ID of the connection object for the service where the customer originates',
	},
	{
		displayName: 'Customer ID',
		name: 'externalid',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['ecommerceCustomer'],
			},
		},
		description: 'The ID of the customer in the external service',
	},
	{
		displayName: 'Customer Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['ecommerceCustomer'],
			},
		},
		description: 'The email address of the customer',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['ecommerceCustomer'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Accepts Marketing',
				name: 'acceptsMarketing',
				type: 'boolean',
				default: false,
				description: 'Whether customer has opt-ed in to marketing communications',
			},
		],
	},

	// ----------------------------------
	//         ecommerceCustomer:update
	// ----------------------------------
	{
		displayName: 'Customer ID',
		name: 'ecommerceCustomerId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['ecommerceCustomer'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the E-commerce customer to update',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		description: 'The fields to update',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['ecommerceCustomer'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Service ID',
				name: 'connectionid',
				type: 'string',
				default: '',
				description:
					'The ID of the connection object for the service where the customer originates',
			},
			{
				displayName: 'Customer ID',
				name: 'externalid',
				type: 'string',
				default: '',
				description: 'The ID of the customer in the external service',
			},
			{
				displayName: 'Customer Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
				description: 'The email address of the customer',
			},
			{
				displayName: 'Accepts Marketing',
				name: 'acceptsMarketing',
				type: 'boolean',
				default: false,
				description: 'Whether customer has opt-ed in to marketing communications',
			},
		],
	},

	// ----------------------------------
	//         ecommerceCustomer:delete
	// ----------------------------------
	{
		displayName: 'Customer ID',
		name: 'ecommerceCustomerId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['ecommerceCustomer'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the E-commerce customer to delete',
	},

	// ----------------------------------
	//         ecommerceCustomer:get
	// ----------------------------------
	{
		displayName: 'Customer ID',
		name: 'ecommerceCustomerId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['ecommerceCustomer'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the E-commerce customer to get',
	},

	// ----------------------------------
	//         ecommerceCustomer:getAll
	// ----------------------------------
	...activeCampaignDefaultGetAllProperties('ecommerceCustomer', 'getAll'),
];
