"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Iterable/UserListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Iterable 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userListOperations、userListFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Iterable/UserListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Iterable/UserListDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userListOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['userList'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add user to list',
				action: 'Add a user to a list',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a user from a list',
				action: 'Remove a user from a list',
			},
		],
		default: 'add',
	},
];

export const userListFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                userList:add                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List Name or ID',
		name: 'listId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLists',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['add'],
			},
		},
		default: '',
		description:
			'Identifier to be used. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Identifier',
		name: 'identifier',
		type: 'options',
		required: true,
		options: [
			{
				name: 'Email',
				value: 'email',
			},
			{
				name: 'User ID',
				value: 'userId',
			},
		],
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['add'],
			},
		},
		default: '',
		description: 'Identifier to be used',
	},
	{
		displayName: 'Value',
		name: 'value',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['add'],
			},
		},
		default: '',
	},

	/* -------------------------------------------------------------------------- */
	/*                                userList:remove                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List Name or ID',
		name: 'listId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLists',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['remove'],
			},
		},
		default: '',
		description:
			'Identifier to be used. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Identifier',
		name: 'identifier',
		type: 'options',
		required: true,
		options: [
			{
				name: 'Email',
				value: 'email',
			},
			{
				name: 'User ID',
				value: 'userId',
			},
		],
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['remove'],
			},
		},
		default: '',
		description: 'Identifier to be used',
	},
	{
		displayName: 'Value',
		name: 'value',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['remove'],
			},
		},
		default: '',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['userList'],
				operation: ['remove'],
			},
		},
		options: [
			{
				displayName: 'Campaign ID',
				name: 'campaignId',
				type: 'number',
				default: 0,
				description: 'Attribute unsubscribe to a campaign',
			},
			{
				displayName: 'Channel Unsubscribe',
				name: 'channelUnsubscribe',
				type: 'boolean',
				default: false,
				description:
					"Whether to unsubscribe email from list's associated channel - essentially a global unsubscribe",
			},
		],
	},
];
