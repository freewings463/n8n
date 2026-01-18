"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UnleashedSoftware/StockOnHandDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UnleashedSoftware 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:stockOnHandOperations、stockOnHandFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UnleashedSoftware/StockOnHandDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UnleashedSoftware/StockOnHandDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const stockOnHandOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['stockOnHand'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a stock on hand',
				action: 'Get a stock on hand',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many stocks on hand',
				action: 'Get many stocks on hand',
			},
		],
		default: 'getAll',
	},
];

export const stockOnHandFields: INodeProperties[] = [
	/* ------------------------------------------------------------------------- */
	/*                                stockOnHand:get                            */
	/* ------------------------------------------------------------------------- */
	{
		displayName: 'Product ID',
		name: 'productId',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['stockOnHand'],
			},
		},
		default: '',
	},
	/* ------------------------------------------------------------------------- */
	/*                                stockOnHand:getAll                         */
	/* ------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['stockOnHand'],
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
				resource: ['stockOnHand'],
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
				resource: ['stockOnHand'],
			},
		},
		options: [
			{
				displayName: 'As at Date',
				name: 'asAtDate',
				type: 'dateTime',
				default: '',
				description: 'Returns the stock on hand for a specific date',
			},
			{
				displayName: 'Is Assembled',
				name: 'IsAssembled',
				type: 'boolean',
				default: false,
				description:
					'Whether the AvailableQty will also include the quantity that can be assembled',
			},
			{
				displayName: 'Modified Since',
				name: 'modifiedSince',
				type: 'dateTime',
				default: '',
				description: 'Returns stock on hand values modified after a specific date',
			},
			{
				displayName: 'Order By',
				name: 'orderBy',
				type: 'string',
				default: '',
				description:
					'Orders the list by a specific column, by default the list is ordered by productCode',
			},
			{
				displayName: 'Product ID',
				name: 'productId',
				type: 'string',
				default: '',
				description:
					'Returns products with the specific Product Guid. You can enter multiple product IDs separated by commas.',
			},
			{
				displayName: 'Warehouse Code',
				name: 'warehouseCode',
				type: 'string',
				default: '',
				description: 'Returns stock on hand for a specific warehouse code',
			},
			{
				displayName: 'Warehouse Name',
				name: 'warehouseName',
				type: 'string',
				default: '',
				description: 'Returns stock on hand for a specific warehouse name',
			},
		],
	},
];
