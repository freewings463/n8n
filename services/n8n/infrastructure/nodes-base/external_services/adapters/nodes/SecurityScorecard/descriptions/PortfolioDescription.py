"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SecurityScorecard/descriptions/PortfolioDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SecurityScorecard/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:portfolioOperations、portfolioFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SecurityScorecard/descriptions/PortfolioDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SecurityScorecard/descriptions/PortfolioDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const portfolioOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		displayOptions: {
			show: {
				resource: ['portfolio'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a portfolio',
				action: 'Create a portfolio',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a portfolio',
				action: 'Delete a portfolio',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many portfolios',
				action: 'Get many portfolios',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a portfolio',
				action: 'Update a portfolio',
			},
		],
		default: 'create',
	},
];

export const portfolioFields: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['portfolio'],
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
				resource: ['portfolio'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Portfolio ID',
		name: 'portfolioId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['portfolio'],
				operation: ['update', 'delete'],
			},
		},
	},
	{
		displayName: 'Portfolio Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['portfolio'],
				operation: ['create', 'update'],
			},
		},
		description: 'Name of the portfolio',
	},
	{
		displayName: 'Description',
		name: 'description',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['portfolio'],
				operation: ['create', 'update'],
			},
		},
	},
	{
		displayName: 'Privacy',
		name: 'privacy',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['portfolio'],
				operation: ['create', 'update'],
			},
		},
		options: [
			{
				name: 'Private',
				value: 'private',
				description: 'Only visible to you',
			},
			{
				name: 'Shared',
				value: 'shared',
				description: 'Visible to everyone in your company',
			},
			{
				name: 'Team',
				value: 'team',
				description: 'Visible to the people on your team',
			},
		],
		default: 'shared',
	},
];
