"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActiveCampaign/EcomOrderProductsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActiveCampaign 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:ecomOrderProductsOperations、ecomOrderProductsFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActiveCampaign/EcomOrderProductsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActiveCampaign/EcomOrderProductsDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { activeCampaignDefaultGetAllProperties } from './GenericFunctions';

export const ecomOrderProductsOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['ecommerceOrderProducts'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get data of many order products',
				action: 'Get many ecommerce orders',
			},
			{
				name: 'Get by Product ID',
				value: 'getByProductId',
				description: 'Get data of a ordered product',
				action: 'Get an e-commerce order product by product ID',
			},
			{
				name: 'Get by Order ID',
				value: 'getByOrderId',
				description: "Get data of an order's products",
				action: 'Get an e-commerce order product by order ID',
			},
		],
		default: 'getAll',
	},
];

export const ecomOrderProductsFields: INodeProperties[] = [
	// ----------------------------------
	//         ecommerceOrderProducts:getByOrderId
	// ----------------------------------
	{
		displayName: 'Order ID',
		name: 'orderId',
		type: 'number',
		default: 0,
		displayOptions: {
			show: {
				operation: ['getByOrderId'],
				resource: ['ecommerceOrderProducts'],
			},
		},
		description: "The ID of the order whose products you'd like returned",
	},

	// ----------------------------------
	//         ecommerceOrderProducts:getByProductId
	// ----------------------------------
	{
		displayName: 'Product ID',
		name: 'procuctId',
		type: 'number',
		default: 0,
		displayOptions: {
			show: {
				operation: ['getByProductId'],
				resource: ['ecommerceOrderProducts'],
			},
		},
		description: "The ID of the product you'd like returned",
	},

	// ----------------------------------
	//         ecommerceOrderProducts:getAll
	// ----------------------------------
	...activeCampaignDefaultGetAllProperties('ecommerceOrderProducts', 'getAll'),
];
