"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Netlify/SiteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Netlify 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:siteOperations、siteFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Netlify/SiteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Netlify/SiteDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const siteOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['site'],
			},
		},
		options: [
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a site',
				action: 'Delete a site',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a site',
				action: 'Get a site',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Returns many sites',
				action: 'Get many sites',
			},
		],
		default: 'delete',
	},
];

export const siteFields: INodeProperties[] = [
	{
		displayName: 'Site ID',
		name: 'siteId',
		required: true,
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['get', 'delete'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['site'],
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
				resource: ['site'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 200,
		},
		default: 50,
		description: 'Max number of results to return',
	},
];
