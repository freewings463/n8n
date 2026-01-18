"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SecurityScorecard/descriptions/IndustryDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SecurityScorecard/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:industryOperations、industryFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SecurityScorecard/descriptions/IndustryDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SecurityScorecard/descriptions/IndustryDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const industryOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		displayOptions: {
			show: {
				resource: ['industry'],
			},
		},
		options: [
			{
				name: 'Get Factor Scores',
				value: 'getFactor',
				action: 'Get factor scores for an industry',
			},
			{
				name: 'Get Historical Factor Scores',
				value: 'getFactorHistorical',
				action: 'Get historical factor scores for an industry',
			},
			{
				name: 'Get Score',
				value: 'getScore',
				action: 'Get the score for an industry',
			},
		],
		default: 'getFactor',
	},
];

export const industryFields: INodeProperties[] = [
	{
		displayName: 'Industry',
		name: 'industry',
		type: 'options',
		default: 'food',
		options: [
			{
				name: 'Food',
				value: 'food',
			},
			{
				name: 'Healthcare',
				value: 'healthcare',
			},
			{
				name: 'Manofacturing',
				value: 'manofacturing',
			},
			{
				name: 'Retail',
				value: 'retail',
			},
			{
				name: 'Technology',
				value: 'technology',
			},
		],
		required: true,
		displayOptions: {
			show: {
				resource: ['industry'],
				operation: ['getScore', 'getFactor', 'getFactorHistorical'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['industry'],
				operation: ['getFactor', 'getFactorHistorical'],
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
				resource: ['industry'],
				operation: ['getFactor', 'getFactorHistorical'],
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
				resource: ['industry'],
				operation: ['getFactor', 'getFactorHistorical'],
			},
		},
		default: true,
		description: 'Whether to return a simplified version of the response instead of the raw data',
	},
	{
		displayName: 'Options',
		name: 'options',
		displayOptions: {
			show: {
				resource: ['industry'],
				operation: ['getFactorHistorical'],
			},
		},
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Date From',
				description: 'History start date',
				name: 'from',
				type: 'dateTime',
				default: '',
			},
			{
				displayName: 'Date To',
				description: 'History end date',
				name: 'to',
				type: 'dateTime',
				default: '',
			},
		],
	},
];
