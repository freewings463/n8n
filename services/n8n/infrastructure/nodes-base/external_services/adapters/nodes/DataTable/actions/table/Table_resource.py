"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/actions/table/Table.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./list.operation、./update.operation 等1项。导出:create、deleteTable、list、update、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/actions/table/Table.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/actions/table/Table_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteTable from './delete.operation';
import * as list from './list.operation';
import * as update from './update.operation';
import { DATA_TABLE_RESOURCE_LOCATOR_BASE } from '../../common/fields';

export { create, deleteTable, list, update };

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
				name: 'Create',
				value: create.FIELD,
				description: 'Create a new data table',
				action: 'Create a data table',
			},
			{
				name: 'Delete',
				value: deleteTable.FIELD,
				description: 'Delete a data table',
				action: 'Delete a data table',
			},
			{
				name: 'List',
				value: list.FIELD,
				description: 'List all data tables',
				action: 'List data tables',
			},
			{
				name: 'Update',
				value: update.FIELD,
				description: 'Update a data table name',
				action: 'Update a data table',
			},
		],
		default: 'list',
	},
	{
		...DATA_TABLE_RESOURCE_LOCATOR_BASE,
		displayOptions: {
			show: {
				resource: ['table'],
				operation: [deleteTable.FIELD, update.FIELD],
			},
		},
	},
	...create.description,
	...deleteTable.description,
	...list.description,
	...update.description,
];
