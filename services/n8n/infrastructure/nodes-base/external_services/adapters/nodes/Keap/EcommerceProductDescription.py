"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Keap/EcommerceProductDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Keap 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ecommerceProductOperations、ecommerceProductFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Keap/EcommerceProductDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Keap/EcommerceProductDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const ecommerceProductOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['ecommerceProduct'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an ecommerce product',
				action: 'Create an e-commerce product',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an ecommerce product',
				action: 'Delete an e-commerce product',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get an ecommerce product',
				action: 'Get an e-commerce product',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many ecommerce products',
				action: 'Get many e-commerce products',
			},
		],
		default: 'create',
	},
];

export const ecommerceProductFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 ecommerceProduct:create                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Product Name',
		name: 'productName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['ecommerceProduct'],
			},
		},
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
				operation: ['create'],
				resource: ['ecommerceProduct'],
			},
		},
		options: [
			{
				displayName: 'Active',
				name: 'active',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Product Description',
				name: 'productDesc',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Product Price',
				name: 'productPrice',
				type: 'number',
				typeOptions: {
					minValue: 0,
				},
				default: 0,
			},
			{
				displayName: 'Product Short Desc',
				name: 'productShortDesc',
				type: 'string',
				default: '',
			},
			{
				displayName: 'SKU',
				name: 'sku',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Subscription Only',
				name: 'subscriptionOnly',
				type: 'boolean',
				default: false,
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                 ecommerceProduct:delete                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Product ID',
		name: 'productId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['ecommerceProduct'],
			},
		},
		default: '',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 ecommerceProduct:get                       */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Product ID',
		name: 'productId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['ecommerceProduct'],
			},
		},
		default: '',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 ecommerceProduct:getAll                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['ecommerceProduct'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['ecommerceProduct'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 200,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['ecommerceProduct'],
			},
		},
		options: [
			{
				displayName: 'Active',
				name: 'active',
				type: 'boolean',
				default: false,
			},
		],
	},
];
