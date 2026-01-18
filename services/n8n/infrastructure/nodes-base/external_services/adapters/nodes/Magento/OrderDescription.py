"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Magento/OrderDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Magento 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:orderOperations、orderFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Magento/OrderDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Magento/OrderDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { getSearchFilters } from './GenericFunctions';

export const orderOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['order'],
			},
		},
		options: [
			{
				name: 'Cancel',
				value: 'cancel',
				description: 'Cancel an order',
				action: 'Cancel an order',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get an order',
				action: 'Get an order',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many orders',
				action: 'Get many orders',
			},
			{
				name: 'Ship',
				value: 'ship',
				description: 'Ship an order',
				action: 'Ship an order',
			},
		],
		default: 'cancel',
	},
];

export const orderFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   order:cancel			                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Order ID',
		name: 'orderId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['order'],
				operation: ['cancel', 'get', 'ship'],
			},
		},
	},

	/* -------------------------------------------------------------------------- */
	/*                                   order:getAll			                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['order'],
				operation: ['getAll'],
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
				resource: ['order'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 10,
		},
		default: 5,
		description: 'Max number of results to return',
	},
	...getSearchFilters('order', 'getOrderAttributes', 'getOrderAttributes'),
];
