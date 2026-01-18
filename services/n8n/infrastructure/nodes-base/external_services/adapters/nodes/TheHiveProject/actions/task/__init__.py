"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/task/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteTask.operation、./executeResponder.operation、./get.operation 等2项。导出:create、deleteTask、executeResponder、get、search、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/task/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/task/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteTask from './deleteTask.operation';
import * as executeResponder from './executeResponder.operation';
import * as get from './get.operation';
import * as search from './search.operation';
import * as update from './update.operation';

export { create, deleteTask, executeResponder, get, search, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		default: 'create',
		type: 'options',
		noDataExpression: true,
		required: true,
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a task',
			},
			{
				name: 'Delete',
				value: 'deleteTask',
				action: 'Delete an task',
			},
			{
				name: 'Execute Responder',
				value: 'executeResponder',
				action: 'Execute responder on a task',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a task',
			},
			{
				name: 'Search',
				value: 'search',
				action: 'Search tasks',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a task',
			},
		],
		displayOptions: {
			show: {
				resource: ['task'],
			},
		},
	},
	...create.description,
	...deleteTask.description,
	...executeResponder.description,
	...get.description,
	...search.description,
	...update.description,
];
