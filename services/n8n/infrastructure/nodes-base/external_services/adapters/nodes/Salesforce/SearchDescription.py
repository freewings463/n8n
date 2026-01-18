"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesforce/SearchDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesforce 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:searchOperations、searchFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesforce/SearchDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesforce/SearchDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const searchOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['search'],
			},
		},
		options: [
			{
				name: 'Query',
				value: 'query',
				description: 'Execute a SOQL query that returns all the results in a single response',
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
		displayName: 'Query',
		name: 'query',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['search'],
				operation: ['query'],
			},
		},
		description:
			'A SOQL query. An example query parameter string might look like: “SELECT+Name+FROM+MyObject”. If the SOQL query string is invalid, a MALFORMED_QUERY response is returned.',
	},
];
