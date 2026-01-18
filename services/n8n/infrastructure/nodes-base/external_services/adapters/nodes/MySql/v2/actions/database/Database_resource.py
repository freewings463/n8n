"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/actions/database/Database.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./deleteTable.operation、./executeQuery.operation、./insert.operation、./select.operation 等3项。导出:deleteTable、executeQuery、insert、select、update、upsert、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/actions/database/Database.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/actions/database/Database_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as deleteTable from './deleteTable.operation';
import * as executeQuery from './executeQuery.operation';
import * as insert from './insert.operation';
import * as select from './select.operation';
import * as update from './update.operation';
import * as upsert from './upsert.operation';
import { tableRLC } from '../common.descriptions';

export { deleteTable, executeQuery, insert, select, update, upsert };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Delete',
				value: 'deleteTable',
				description: 'Delete an entire table or rows in a table',
				action: 'Delete table or rows',
			},
			{
				name: 'Execute SQL',
				value: 'executeQuery',
				description: 'Execute an SQL query',
				action: 'Execute a SQL query',
			},
			{
				name: 'Insert',
				value: 'insert',
				description: 'Insert rows in a table',
				action: 'Insert rows in a table',
			},
			{
				// eslint-disable-next-line n8n-nodes-base/node-param-option-name-wrong-for-upsert
				name: 'Insert or Update',
				value: 'upsert',
				// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-upsert
				description: 'Insert or update rows in a table',
				action: 'Insert or update rows in a table',
			},
			{
				name: 'Select',
				value: 'select',
				description: 'Select rows from a table',
				action: 'Select rows from a table',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update rows in a table',
				action: 'Update rows in a table',
			},
		],
		displayOptions: {
			show: {
				resource: ['database'],
			},
		},
		default: 'insert',
	},
	{
		...tableRLC,
		displayOptions: { hide: { operation: ['executeQuery'] } },
	},
	...deleteTable.description,
	...executeQuery.description,
	...insert.description,
	...select.description,
	...update.description,
	...upsert.description,
];
