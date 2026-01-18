"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discourse/SearchDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discourse 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:searchOperations、searchFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discourse/SearchDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discourse/SearchDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const searchOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		description: 'Choose an operation',
		required: true,
		displayOptions: {
			show: {
				resource: ['search'],
			},
		},
		options: [
			{
				name: 'Query',
				value: 'query',
				description: 'Search for something',
				action: 'Perform a query',
			},
		],
		default: 'query',
	},
];

export const searchFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                search:query                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Term',
		name: 'term',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['search'],
				operation: ['query'],
			},
		},
		default: '',
		description: 'Term to search for',
	},
	{
		displayName: 'Simplify',
		name: 'simple',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['search'],
				operation: ['query'],
			},
		},
		default: true,
		description: 'Whether to return a simplified version of the response instead of the raw data',
	},
];
