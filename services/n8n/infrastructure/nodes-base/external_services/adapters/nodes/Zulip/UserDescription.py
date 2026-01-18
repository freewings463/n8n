"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zulip/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zulip 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zulip/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zulip/UserDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a user',
				action: 'Create a user',
			},
			{
				name: 'Deactivate',
				value: 'deactivate',
				description: 'Deactivate a user',
				action: 'Deactivate a user',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a user',
				action: 'Get a user',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many users',
				action: 'Get many users',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a user',
				action: 'Update a user',
			},
		],
		default: 'create',
	},
];

export const userFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                  user:create                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		default: '',
		description: 'The email address of the new user',
	},
	{
		displayName: 'Full Name',
		name: 'fullName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		default: '',
		description: 'The full name of the new user',
	},
	{
		displayName: 'Password',
		name: 'password',
		type: 'string',
		typeOptions: { password: true },
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		default: '',
		description: 'The password of the new user',
	},
	{
		displayName: 'Short Name',
		name: 'shortName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		default: '',
		description: 'The short name of the new user. Not user-visible.',
	},

	/* -------------------------------------------------------------------------- */
	/*                                  user:get / getAll                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
			},
		},
		default: '',
		description: 'The ID of user to get',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get', 'getAll'],
			},
		},
		options: [
			{
				displayName: 'Client Gravatar',
				name: 'clientGravatar',
				type: 'boolean',
				default: false,
				description:
					'Whether the client supports computing gravatars URLs. If enabled, avatar_url will be included in the response only if there is a Zulip avatar, and will be null for users who are using gravatar as their avatar.',
			},
			{
				displayName: 'Custom Profile Fields',
				name: 'includeCustomProfileFields',
				type: 'boolean',
				default: false,
				description:
					'Whether the client wants custom profile field data to be included in the response',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                  user:update                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['update'],
			},
		},
		default: '',
		description: 'The ID of user to update',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Full Name',
				name: 'fullName',
				type: 'string',
				default: '',
				description: 'The users full name',
			},
			{
				displayName: 'Is Admin',
				name: 'isAdmin',
				type: 'boolean',
				default: false,
				description: 'Whether the target user is an administrator',
			},
			{
				displayName: 'Is Guest',
				name: 'isGuest',
				type: 'boolean',
				default: false,
				description: 'Whether the target user is a guest',
			},
			{
				displayName: 'Profile Data',
				name: 'profileData',
				type: 'fixedCollection',
				default: {},
				description:
					'A dictionary containing the to be updated custom profile field data for the user',
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						displayName: 'Property',
						name: 'property',
						values: [
							{
								displayName: 'ID',
								name: 'id',
								type: 'string',
								required: true,
								default: '',
								description: 'ID of custom profile data value',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								default: '',
								description: 'Value of custom profile data',
							},
						],
					},
				],
			},
			{
				displayName: 'Role',
				name: 'role',
				type: 'options',
				options: [
					{
						name: 'Guest',
						value: 600,
					},
					{
						name: 'Member',
						value: 400,
					},
					{
						name: 'Organization Administrator',
						value: 200,
					},
					{
						name: 'Organization Moderator',
						value: 300,
					},
					{
						name: 'Organization Owner',
						value: 100,
					},
				],
				default: '',
				description: 'Role for the user',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                  user:deactivate                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['deactivate'],
			},
		},
		default: '',
		description: 'The ID of user to deactivate',
	},
];
