"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Stripe/descriptions/TokenDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Stripe/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:tokenOperations、tokenFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Stripe/descriptions/TokenDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Stripe/descriptions/TokenDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const tokenOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'create',
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a token',
				action: 'Create a token',
			},
		],
		displayOptions: {
			show: {
				resource: ['token'],
			},
		},
	},
];

export const tokenFields: INodeProperties[] = [
	// ----------------------------------
	//          token: create
	// ----------------------------------
	{
		displayName: 'Type',
		name: 'type',
		type: 'options',
		required: true,
		default: 'cardToken',
		description: 'Type of token to create',
		options: [
			{
				name: 'Card Token',
				value: 'cardToken',
			},
		],
		displayOptions: {
			show: {
				resource: ['token'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Card Number',
		name: 'number',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['token'],
				operation: ['create'],
				type: ['cardToken'],
			},
		},
		placeholder: '4242424242424242',
		default: '',
	},
	{
		displayName: 'CVC',
		name: 'cvc',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['token'],
				operation: ['create'],
				type: ['cardToken'],
			},
		},
		default: '',
		placeholder: '314',
		description: 'Security code printed on the back of the card',
	},
	{
		displayName: 'Expiration Month',
		description: 'Number of the month when the card will expire',
		name: 'expirationMonth',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['token'],
				operation: ['create'],
				type: ['cardToken'],
			},
		},
		default: '',
		placeholder: '10',
	},
	{
		displayName: 'Expiration Year',
		description: 'Year when the card will expire',
		name: 'expirationYear',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['token'],
				operation: ['create'],
				type: ['cardToken'],
			},
		},
		default: '',
		placeholder: '2022',
	},
];
