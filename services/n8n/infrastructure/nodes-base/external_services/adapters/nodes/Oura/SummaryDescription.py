"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oura/SummaryDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oura 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:summaryOperations、summaryFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oura/SummaryDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oura/SummaryDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const summaryOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['summary'],
			},
		},
		options: [
			{
				name: 'Get Activity Summary',
				value: 'getActivity',
				description: "Get the user's activity summary",
				action: 'Get activity summary',
			},
			{
				name: 'Get Readiness Summary',
				value: 'getReadiness',
				description: "Get the user's readiness summary",
				action: 'Get readiness summary',
			},
			{
				name: 'Get Sleep Periods',
				value: 'getSleep',
				description: "Get the user's sleep summary",
				action: 'Get sleep summary',
			},
		],
		default: 'getSleep',
	},
];

export const summaryFields: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['summary'],
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
				resource: ['summary'],
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
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		displayOptions: {
			show: {
				resource: ['summary'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'End Date',
				name: 'end',
				type: 'dateTime',
				default: '',
				description:
					'End date for the summary retrieval. If omitted, it defaults to the current day.',
			},
			{
				displayName: 'Start Date',
				name: 'start',
				type: 'dateTime',
				default: '',
				description: 'Start date for the summary retrieval. If omitted, it defaults to a week ago.',
			},
		],
	},
];
