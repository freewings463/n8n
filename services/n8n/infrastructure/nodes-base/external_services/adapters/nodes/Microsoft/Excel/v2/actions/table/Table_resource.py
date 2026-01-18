"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/table/Table.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./addTable.operation、./append.operation、./convertToRange.operation、./deleteTable.operation 等3项。导出:append、addTable、convertToRange、deleteTable、getColumns、getRows、lookup、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/table/Table.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/actions/table/Table_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as addTable from './addTable.operation';
import * as append from './append.operation';
import * as convertToRange from './convertToRange.operation';
import * as deleteTable from './deleteTable.operation';
import * as getColumns from './getColumns.operation';
import * as getRows from './getRows.operation';
import * as lookup from './lookup.operation';

export { append, addTable, convertToRange, deleteTable, getColumns, getRows, lookup };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['table'],
			},
		},
		options: [
			{
				name: 'Append',
				value: 'append',
				description: 'Add rows to the end of the table',
				action: 'Append rows to table',
			},
			{
				name: 'Convert to Range',
				value: 'convertToRange',
				description: 'Convert a table to a range',
				action: 'Convert to range',
			},
			{
				name: 'Create',
				value: 'addTable',
				description: 'Add a table based on range',
				action: 'Create a table',
			},
			{
				name: 'Delete',
				value: 'deleteTable',
				description: 'Delete a table',
				action: 'Delete a table',
			},
			{
				name: 'Get Columns',
				value: 'getColumns',
				description: 'Retrieve a list of table columns',
				action: 'Get columns',
			},
			{
				name: 'Get Rows',
				value: 'getRows',
				description: 'Retrieve a list of table rows',
				action: 'Get rows',
			},
			{
				name: 'Lookup',
				value: 'lookup',
				description: 'Look for rows that match a given value in a column',
				action: 'Lookup a column',
			},
		],
		default: 'append',
	},
	...append.description,
	...addTable.description,
	...convertToRange.description,
	...deleteTable.description,
	...getColumns.description,
	...getRows.description,
	...lookup.description,
];
