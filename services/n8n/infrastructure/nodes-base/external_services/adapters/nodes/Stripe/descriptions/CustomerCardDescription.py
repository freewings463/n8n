"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Stripe/descriptions/CustomerCardDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Stripe/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:customerCardOperations、customerCardFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Stripe/descriptions/CustomerCardDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Stripe/descriptions/CustomerCardDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const customerCardOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add a customer card',
				action: 'Add a customer card',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a customer card',
				action: 'Get a customer card',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a customer card',
				action: 'Remove a customer card',
			},
		],
		displayOptions: {
			show: {
				resource: ['customerCard'],
			},
		},
	},
];

export const customerCardFields: INodeProperties[] = [
	// ----------------------------------
	//        customerCard: add
	// ----------------------------------
	{
		displayName: 'Customer ID',
		name: 'customerId',
		type: 'string',
		required: true,
		default: '',
		description: 'ID of the customer to be associated with this card',
		displayOptions: {
			show: {
				resource: ['customerCard'],
				operation: ['add'],
			},
		},
	},
	{
		displayName: 'Card Token',
		name: 'token',
		type: 'string',
		typeOptions: { password: true },
		required: true,
		default: '',
		placeholder: 'tok_1IMfKdJhRTnqS5TKQVG1LI9o',
		description: 'Token representing sensitive card information',
		displayOptions: {
			show: {
				resource: ['customerCard'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------
	//       customerCard: remove
	// ----------------------------------
	{
		displayName: 'Customer ID',
		name: 'customerId',
		type: 'string',
		required: true,
		default: '',
		description: 'ID of the customer whose card to remove',
		displayOptions: {
			show: {
				resource: ['customerCard'],
				operation: ['remove'],
			},
		},
	},
	{
		displayName: 'Card ID',
		name: 'cardId',
		type: 'string',
		required: true,
		default: '',
		description: 'ID of the card to remove',
		displayOptions: {
			show: {
				resource: ['customerCard'],
				operation: ['remove'],
			},
		},
	},

	// ----------------------------------
	//         customerCard: get
	// ----------------------------------
	{
		displayName: 'Customer ID',
		name: 'customerId',
		type: 'string',
		required: true,
		default: '',
		description: 'ID of the customer whose card to retrieve',
		displayOptions: {
			show: {
				resource: ['customerCard'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Source ID',
		name: 'sourceId',
		type: 'string',
		required: true,
		default: '',
		description: 'ID of the source to retrieve',
		displayOptions: {
			show: {
				resource: ['customerCard'],
				operation: ['get'],
			},
		},
	},
];
