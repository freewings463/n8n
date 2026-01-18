"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBooks/descriptions/Purchase/PurchaseDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBooks/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:purchaseOperations、purchaseFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBooks/descriptions/Purchase/PurchaseDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBooks/descriptions/Purchase/PurchaseDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const purchaseOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get a purchase',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many purchases',
			},
		],
		displayOptions: {
			show: {
				resource: ['purchase'],
			},
		},
	},
];

export const purchaseFields: INodeProperties[] = [
	// ----------------------------------
	//         purchase: get
	// ----------------------------------
	{
		displayName: 'Purchase ID',
		name: 'purchaseId',
		type: 'string',
		required: true,
		default: '',
		description: 'The ID of the purchase to retrieve',
		displayOptions: {
			show: {
				resource: ['purchase'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//         purchase: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['purchase'],
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
			maxValue: 1000,
		},
		displayOptions: {
			show: {
				resource: ['purchase'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Query',
				name: 'query',
				type: 'string',
				default: '',
				placeholder: "WHERE Metadata.LastUpdatedTime > '2021-01-01'",
				description:
					'The condition for selecting purchases. See the <a href="https://developer.intuit.com/app/developer/qbo/docs/develop/explore-the-quickbooks-online-api/data-queries">guide</a> for supported syntax.',
			},
		],
		displayOptions: {
			show: {
				resource: ['purchase'],
				operation: ['getAll'],
			},
		},
	},
];
