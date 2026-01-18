"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Matrix/RoomDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Matrix 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:roomOperations、roomFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Matrix/RoomDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Matrix/RoomDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const roomOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['room'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'New chat room with defined settings',
				action: 'Create a room',
			},
			{
				name: 'Invite',
				value: 'invite',
				description: 'Invite a user to a room',
				action: 'Invite a room',
			},
			{
				name: 'Join',
				value: 'join',
				description: 'Join a new room',
				action: 'Join a room',
			},
			{
				name: 'Kick',
				value: 'kick',
				description: 'Kick a user from a room',
				action: 'Kick a user from a room',
			},
			{
				name: 'Leave',
				value: 'leave',
				description: 'Leave a room',
				action: 'Leave a room',
			},
		],
		default: 'create',
	},
];

export const roomFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                room:create                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Room Name',
		name: 'roomName',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['create'],
			},
		},
		default: '',
		placeholder: 'My new room',
		required: true,
	},
	{
		displayName: 'Preset',
		name: 'preset',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['create'],
			},
		},
		options: [
			{
				name: 'Private Chat',
				value: 'private_chat',
			},
			{
				name: 'Public Chat',
				value: 'public_chat',
				description: 'Open and public chat',
			},
		],
		default: 'public_chat',
		placeholder: 'My new room',
		required: true,
	},
	{
		displayName: 'Room Alias',
		name: 'roomAlias',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['create'],
			},
		},
		default: '',
		placeholder: 'coolest-room-around',
	},
	/* -------------------------------------------------------------------------- */
	/*                                  room:join                                 */
	/* -------------------------------------------------------------------------- */

	{
		displayName: 'Room ID or Alias',
		name: 'roomIdOrAlias',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['join'],
			},
		},
		default: '',
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                  room:leave                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Room Name or ID',
		name: 'roomId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['leave'],
			},
		},
		default: '',
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                 room:invite                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Room Name or ID',
		name: 'roomId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['invite'],
			},
		},
		default: '',
		required: true,
	},

	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['invite'],
			},
		},
		default: '',
		description: 'The fully qualified user ID of the invitee',
		placeholder: '@cheeky_monkey:matrix.org',
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                  room:kick                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Room Name or ID',
		name: 'roomId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['kick'],
			},
		},
		default: '',
		required: true,
	},
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['kick'],
			},
		},
		default: '',
		description: 'The fully qualified user ID',
		placeholder: '@cheeky_monkey:matrix.org',
		required: true,
	},
	{
		displayName: 'Reason',
		name: 'reason',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['room'],
				operation: ['kick'],
			},
		},
		default: '',
		description: 'Reason for kick',
		placeholder: 'Telling unfunny jokes',
	},
];
