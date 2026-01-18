"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SecurityScorecard/descriptions/PortfolioCompanyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SecurityScorecard/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:portfolioCompanyOperations、portfolioCompanyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SecurityScorecard/descriptions/PortfolioCompanyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SecurityScorecard/descriptions/PortfolioCompanyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const portfolioCompanyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		displayOptions: {
			show: {
				resource: ['portfolioCompany'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add a company to portfolio',
				action: 'Add a portfolio company',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many companies in a portfolio',
				action: 'Get many portfolio companies',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a company from portfolio',
				action: 'Remove a portfolio company',
			},
		],
		default: 'add',
	},
];

export const portfolioCompanyFields: INodeProperties[] = [
	{
		displayName: 'Portfolio ID',
		name: 'portfolioId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['portfolioCompany'],
				operation: ['getAll', 'add', 'remove'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['portfolioCompany'],
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
				resource: ['portfolioCompany'],
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
		displayName: 'Filters',
		name: 'filters',
		displayOptions: {
			show: {
				resource: ['portfolioCompany'],
				operation: ['getAll'],
			},
		},
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		options: [
			{
				displayName: 'Grade',
				name: 'grade',
				type: 'string',
				placeholder: '',
				default: '',
				description: 'Company score grade filter',
			},
			{
				displayName: 'Industry',
				name: 'industry',
				type: 'string',
				placeholder: '',
				default: '',
				description: 'Industry filter',
			},
			{
				displayName: 'Issue Type',
				name: 'issueType',
				type: 'string',
				placeholder: '',
				description: 'Issue type filter',
				default: '',
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				options: [
					{
						name: 'Active',
						value: 'active',
					},
					{
						name: 'Inactive',
						value: 'inactive',
					},
				],
				default: '',
			},
			{
				displayName: 'Vulnerability',
				name: 'vulnerability',
				type: 'string',
				placeholder: '',
				description: 'CVE vulnerability filter',
				default: '',
			},
		],
	},
	{
		displayName: 'Domain',
		name: 'domain',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['portfolioCompany'],
				operation: ['add', 'remove'],
			},
		},
		description: "Company's domain name",
	},
];
