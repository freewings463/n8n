"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discourse/UserGroupDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discourse 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userGroupOperations、userGroupFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discourse/UserGroupDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discourse/UserGroupDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userGroupOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		description: 'Choose an operation',
		required: true,
		displayOptions: {
			show: {
				resource: ['userGroup'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Create a user to group',
				action: 'Add a user to a group',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove user from group',
				action: 'Remove a user from a group',
			},
		],
		default: 'add',
	},
];

export const userGroupFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                userGroup:add                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Usernames',
		name: 'usernames',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['userGroup'],
				operation: ['add'],
			},
		},
		default: '',
		description: 'Usernames to add to group. Multiples can be defined separated by comma.',
	},
	{
		displayName: 'Group ID',
		name: 'groupId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['userGroup'],
				operation: ['add'],
			},
		},
		default: '',
		description: 'ID of the group',
	},

	/* -------------------------------------------------------------------------- */
	/*                                userGroup:remove                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Usernames',
		name: 'usernames',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['userGroup'],
				operation: ['remove'],
			},
		},
		default: '',
		description: 'Usernames to remove from group. Multiples can be defined separated by comma.',
	},
	{
		displayName: 'Group ID',
		name: 'groupId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['userGroup'],
				operation: ['remove'],
			},
		},
		default: '',
		description: 'ID of the group to remove',
	},
];
