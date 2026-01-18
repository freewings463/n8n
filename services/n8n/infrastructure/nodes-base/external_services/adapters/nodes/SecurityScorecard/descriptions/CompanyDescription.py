"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SecurityScorecard/descriptions/CompanyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SecurityScorecard/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:companyOperations、companyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SecurityScorecard/descriptions/CompanyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SecurityScorecard/descriptions/CompanyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const companyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		displayOptions: {
			show: {
				resource: ['company'],
			},
		},
		options: [
			{
				name: 'Get Factor Scores',
				value: 'getFactor',
				description: 'Get company factor scores and issue counts',
				action: 'Get a company factor scores and issue counts',
			},
			{
				name: 'Get Historical Factor Scores',
				value: 'getFactorHistorical',
				description: "Get company's historical factor scores",
				action: "Get a company's historical factor scores",
			},
			{
				name: 'Get Historical Scores',
				value: 'getHistoricalScore',
				description: "Get company's historical scores",
				action: "Get a company's historical scores",
			},
			{
				name: 'Get Information and Scorecard',
				value: 'getScorecard',
				description: 'Get company information and summary of their scorecard',
				action: 'Get company information and a summary of their scorecard',
			},
			{
				name: 'Get Score Plan',
				value: 'getScorePlan',
				description: "Get company's score improvement plan",
				action: "Get a company's score improvement plan",
			},
		],
		default: 'getFactor',
	},
];

export const companyFields: INodeProperties[] = [
	{
		displayName: 'Scorecard Identifier',
		name: 'scorecardIdentifier',
		description: 'Primary identifier of a company or scorecard, i.e. domain.',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['company'],
				operation: [
					'getScorecard',
					'getFactor',
					'getFactorHistorical',
					'getHistoricalScore',
					'getScorePlan',
				],
			},
		},
	},
	{
		displayName: 'Score',
		name: 'score',
		description: 'Score target',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['getScorePlan'],
			},
		},
		required: true,
		default: 0,
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['getFactor', 'getFactorHistorical', 'getHistoricalScore', 'getScorePlan'],
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
				resource: ['company'],
				operation: ['getFactor', 'getFactorHistorical', 'getHistoricalScore', 'getScorePlan'],
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
		displayName: 'Simplify',
		name: 'simple',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['getFactorHistorical', 'getHistoricalScore'],
			},
		},
		default: true,
		description: 'Whether to return a simplified version of the response instead of the raw data',
	},

	// company:getFactor
	{
		displayName: 'Filters',
		name: 'filters',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['getFactor'],
			},
		},
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		options: [
			{
				displayName: 'Severity',
				name: 'severity',
				type: 'string',
				default: '',
				placeholder: '',
			},
			{
				displayName: 'Severity In',
				description: 'Filter issues by comma-separated severity list',
				name: 'severity_in',
				type: 'string',
				default: '',
				placeholder: '',
			},
		],
	},

	// company:getFactorHistorical
	// company:getHistoricalScore
	{
		displayName: 'Options',
		name: 'options',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['getFactorHistorical', 'getHistoricalScore'],
			},
		},
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Date From',
				description: 'History start date',
				name: 'date_from',
				type: 'dateTime',
				default: '',
			},
			{
				displayName: 'Date To',
				description: 'History end date',
				name: 'date_to',
				type: 'dateTime',
				default: '',
			},
			{
				displayName: 'Timing',
				description: 'Date granularity',
				name: 'timing',
				type: 'options',
				options: [
					{
						name: 'Daily',
						value: 'daily',
					},
					{
						name: 'Weekly',
						value: 'weekly',
					},
					{
						name: 'Monthly',
						value: 'monthly',
					},
				],
				default: 'daily',
			},
		],
	},
];
