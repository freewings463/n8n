"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/TaskDependencyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:taskDependencyOperations、taskDependencyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/TaskDependencyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/TaskDependencyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const taskDependencyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['taskDependency'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a task dependency',
				action: 'Create a task dependency',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a task dependency',
				action: 'Delete a task dependency',
			},
		],
		default: 'create',
	},
];

export const taskDependencyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                taskDependency:create                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Task ID',
		name: 'task',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskDependency'],
				operation: ['create'],
			},
		},
		required: true,
	},
	{
		displayName: 'Depends On Task ID',
		name: 'dependsOnTask',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskDependency'],
				operation: ['create'],
			},
		},
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                taskDependency:delete                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Task ID',
		name: 'task',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskDependency'],
				operation: ['delete'],
			},
		},
		required: true,
	},
	{
		displayName: 'Depends On Task ID',
		name: 'dependsOnTask',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskDependency'],
				operation: ['delete'],
			},
		},
		required: true,
	},
];
