"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BigQuery/v2/actions/database/Database.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BigQuery 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./executeQuery.operation、./insert.operation、../commonDescriptions/RLC.description。导出:executeQuery、insert、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BigQuery/v2/actions/database/Database.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BigQuery/v2/actions/database/Database_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as executeQuery from './executeQuery.operation';
import * as insert from './insert.operation';
import { datasetRLC, projectRLC, tableRLC } from '../commonDescriptions/RLC.description';

export { executeQuery, insert };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['database'],
			},
		},
		options: [
			{
				name: 'Execute Query',
				value: 'executeQuery',
				description: 'Execute a SQL query',
				action: 'Execute a SQL query',
			},
			{
				name: 'Insert',
				value: 'insert',
				description: 'Insert rows in a table',
				action: 'Insert rows in a table',
			},
		],
		default: 'executeQuery',
	},
	{
		...projectRLC,
		displayOptions: {
			show: {
				resource: ['database'],
				operation: ['executeQuery', 'insert'],
			},
		},
	},
	{
		...datasetRLC,
		displayOptions: {
			show: {
				resource: ['database'],
				operation: ['insert'],
			},
		},
	},
	{
		...tableRLC,
		displayOptions: {
			show: {
				resource: ['database'],
				operation: ['insert'],
			},
		},
	},
	...executeQuery.description,
	...insert.description,
];
