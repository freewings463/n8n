"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/row/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./get.operation、./list.operation、./lock.operation 等5项。导出:create、get、search、update、remove、lock、unlock、list 等1项。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/row/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/row/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as get from './get.operation';
import * as list from './list.operation';
import * as lock from './lock.operation';
import * as remove from './remove.operation';
import * as search from './search.operation';
import { sharedProperties } from './sharedProperties';
import * as unlock from './unlock.operation';
import * as update from './update.operation';

export { create, get, search, update, remove, lock, unlock, list };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['row'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new row',
				action: 'Create a row',
			},
			{
				name: 'Delete',
				value: 'remove',
				description: 'Delete a row',
				action: 'Delete a row',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get the content of a row',
				action: 'Get a row',
			},
			{
				name: 'Get Many',
				value: 'list',
				description: 'Get many rows from a table or a table view',
				action: 'Get many rows',
			},
			{
				name: 'Lock',
				value: 'lock',
				description: 'Lock a row to prevent further changes',
				action: 'Add a row lock',
			},
			{
				name: 'Search',
				value: 'search',
				description: 'Search one or multiple rows',
				action: 'Search a row by keyword',
			},
			{
				name: 'Unlock',
				value: 'unlock',
				description: 'Remove the lock from a row',
				action: 'Remove a row lock',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update the content of a row',
				action: 'Update a row',
			},
		],
		default: 'create',
	},
	...sharedProperties,
	...create.description,
	...get.description,
	...list.description,
	...search.description,
	...update.description,
];
