"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/TaskListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:taskListOperations、taskListFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/TaskListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/TaskListDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const taskListOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['taskList'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add a task to a list',
				action: 'Add a task to a list',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a task from a list',
				action: 'Remove a task from a list',
			},
		],
		default: 'add',
	},
];

export const taskListFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                taskList:add                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Task ID',
		name: 'taskId',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskList'],
				operation: ['remove', 'add'],
			},
		},
		required: true,
	},
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskList'],
				operation: ['remove', 'add'],
			},
		},
		required: true,
	},
];
