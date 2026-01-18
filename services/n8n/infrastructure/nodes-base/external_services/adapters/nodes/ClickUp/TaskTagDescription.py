"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/TaskTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:taskTagOperations、taskTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/TaskTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/TaskTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const taskTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['taskTag'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add a tag to a task',
				action: 'Add a task tag',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a tag from a task',
				action: 'Remove a task tag',
			},
		],
		default: 'add',
	},
];

export const taskTagFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                taskTag:add                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Task ID',
		name: 'taskId',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskTag'],
				operation: ['remove', 'add'],
			},
		},
		required: true,
	},
	{
		displayName: 'Tag Name',
		name: 'tagName',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['taskTag'],
				operation: ['remove', 'add'],
			},
		},
		required: true,
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['taskTag'],
				operation: ['remove', 'add'],
			},
		},
		options: [
			{
				displayName: 'Custom Task IDs',
				name: 'custom_task_ids',
				type: 'boolean',
				default: false,
				description: "Whether to reference a task by it's custom task ID",
			},
			{
				displayName: 'Team Name or ID',
				name: 'team_id',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getTeams',
				},
				default: '',
				description:
					'Only used when the parameter is set to custom_task_ids=true. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
			},
		],
	},
];
