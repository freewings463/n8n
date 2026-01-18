"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UnleashedSoftware/SalesOrderDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UnleashedSoftware 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:salesOrderOperations、salesOrderFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UnleashedSoftware/SalesOrderDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UnleashedSoftware/SalesOrderDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const salesOrderOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['salesOrder'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many sales orders',
				action: 'Get many sales orders',
			},
		],
		default: 'getAll',
	},
];

export const salesOrderFields: INodeProperties[] = [
	/* ------------------------------------------------------------------------- */
	/*                                salesOrder:getAll                          */
	/* ------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['salesOrder'],
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
				resource: ['salesOrder'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['salesOrder'],
			},
		},
		options: [
			{
				displayName: 'Customer ID',
				name: 'customerId',
				type: 'string',
				default: '',
				placeholder: 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
				description:
					'Only returns orders for a specified Customer GUID. The CustomerId can be specified as a list of comma-separated GUIDs.',
			},
			{
				displayName: 'Customer Code',
				name: 'customerCode',
				type: 'string',
				default: '',
				description: 'Returns orders that start with the specific customer code',
			},
			{
				displayName: 'End Date',
				name: 'endDate',
				type: 'dateTime',
				default: '',
				description: 'Returns orders with order date before the specified date. UTC.',
			},
			{
				displayName: 'Modified Since',
				name: 'modifiedSince',
				type: 'dateTime',
				default: '',
				description: 'Returns orders created or edited after a specified date, must be UTC format',
			},
			{
				displayName: 'Order Number',
				name: 'orderNumber',
				type: 'string',
				default: '',
				description:
					'Returns a single order with the specified order number. If set, it overrides all other filters.',
			},
			{
				displayName: 'Order Status',
				name: 'orderStatus',
				type: 'multiOptions',
				options: [
					{
						name: 'Backordered',
						value: 'Backordered',
					},
					{
						name: 'Completed',
						value: 'Completed',
					},
					{
						name: 'Deleted',
						value: 'Deleted',
					},
					{
						name: 'Parked',
						value: 'Parked',
					},
					{
						name: 'Placed',
						value: 'Placed',
					},
				],
				default: [],
				description:
					'Returns orders with the specified status. If no orderStatus filter is specified, then we exclude "Deleted" by default.',
			},
			{
				displayName: 'Start Date',
				name: 'startDate',
				type: 'dateTime',
				default: '',
				description: 'Returns orders with order date after the specified date. UTC.',
			},
		],
	},
];
