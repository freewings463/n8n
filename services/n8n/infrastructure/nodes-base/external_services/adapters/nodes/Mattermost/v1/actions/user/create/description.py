"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/user/create/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:userCreateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/user/create/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/user/create/description.py

import type { UserProperties } from '../../Interfaces';

export const userCreateDescription: UserProperties = [
	{
		displayName: 'Username',
		name: 'username',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		default: '',
	},
	{
		displayName: 'Auth Service',
		name: 'authService',
		type: 'options',
		options: [
			{
				name: 'Email',
				value: 'email',
			},
			{
				name: 'Gitlab',
				value: 'gitlab',
			},
			{
				name: 'Google',
				value: 'google',
			},
			{
				name: 'LDAP',
				value: 'ldap',
			},
			{
				name: 'Office365',
				value: 'office365',
			},
			{
				name: 'SAML',
				value: 'saml',
			},
		],
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		default: '',
	},
	{
		displayName: 'Auth Data',
		name: 'authData',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
			hide: {
				authService: ['email'],
			},
		},
		type: 'string',
		default: '',
	},
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
				authService: ['email'],
			},
		},
	},
	{
		displayName: 'Password',
		name: 'password',
		type: 'string',
		typeOptions: {
			password: true,
		},
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
				authService: ['email'],
			},
		},
		default: '',
		description: 'The password used for email authentication',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['user'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'First Name',
				name: 'first_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Last Name',
				name: 'last_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Locale',
				name: 'locale',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Nickname',
				name: 'nickname',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Notification Settings',
				name: 'notificationUi',
				type: 'fixedCollection',
				placeholder: 'Add Notification Setting',
				default: {},
				typeOptions: {
					multipleValues: false,
				},
				options: [
					{
						displayName: 'Notify',
						name: 'notificationValues',
						values: [
							{
								displayName: 'Channel',
								name: 'channel',
								type: 'boolean',
								default: true,
								description:
									'Whether to enable channel-wide notifications (@channel, @all, etc.), "false" to disable. Defaults to "true".',
							},
							{
								displayName: 'Desktop',
								name: 'desktop',
								type: 'options',
								options: [
									{
										name: 'All',
										value: 'all',
										description: 'Notifications for all activity',
									},
									{
										name: 'Mention',
										value: 'mention',
										description: 'Mentions and direct messages only',
									},
									{
										name: 'None',
										value: 'none',
										description: 'Mentions and direct messages only',
									},
								],
								default: 'all',
							},
							{
								displayName: 'Desktop Sound',
								name: 'desktop_sound',
								type: 'boolean',
								default: true,
								description:
									'Whether to enable sound on desktop notifications, "false" to disable. Defaults to "true".',
							},
							{
								displayName: 'Email',
								name: 'email',
								type: 'boolean',
								default: false,
								description:
									'Whether to enable email notifications, "false" to disable. Defaults to "false".',
							},
							{
								displayName: 'First Name',
								name: 'first_name',
								type: 'boolean',
								default: false,
								description:
									'Whether to enable mentions for first name. Defaults to "true" if a first name is set, "false" otherwise.',
							},
							{
								displayName: 'Mention Keys',
								name: 'mention_keys',
								type: 'string',
								default: '',
								description:
									'A comma-separated list of words to count as mentions. Defaults to username and @username.',
							},
							{
								displayName: 'Push',
								name: 'push',
								type: 'options',
								options: [
									{
										name: 'All',
										value: 'all',
										description: 'Notifications for all activity',
									},
									{
										name: 'Mention',
										value: 'mention',
										description: 'Mentions and direct messages only',
									},
									{
										name: 'None',
										value: 'none',
										description: 'Mentions and direct messages only',
									},
								],
								default: 'mention',
							},
						],
					},
				],
			},
		],
	},
];
