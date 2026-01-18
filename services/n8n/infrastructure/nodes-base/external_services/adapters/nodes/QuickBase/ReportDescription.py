"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBase/ReportDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:reportOperations、reportFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBase/ReportDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBase/ReportDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const reportOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['report'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a report',
				action: 'Get a report',
			},
			{
				name: 'Run',
				value: 'run',
				description: 'Run a report',
				action: 'Run a report',
			},
		],
		default: 'get',
	},
];

export const reportFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                report:get                                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Table ID',
		name: 'tableId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['get'],
			},
		},
		description: 'The table identifier',
	},
	{
		displayName: 'Report ID',
		name: 'reportId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['get'],
			},
		},
		description: 'The identifier of the report, unique to the table',
	},
	/* -------------------------------------------------------------------------- */
	/*                                report:run                                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Table ID',
		name: 'tableId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['run'],
			},
		},
		description: 'The table identifier',
	},
	{
		displayName: 'Report ID',
		name: 'reportId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['run'],
			},
		},
		description: 'The identifier of the report, unique to the table',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['run'],
			},
		},
		default: true,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['run'],
			},
			hide: {
				returnAll: [true],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
