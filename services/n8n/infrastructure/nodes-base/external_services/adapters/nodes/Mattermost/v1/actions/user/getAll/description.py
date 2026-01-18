"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/user/getAll/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:userGetAllDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/user/getAll/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/user/getAll/description.py

import type { UserProperties } from '../../Interfaces';

export const userGetAllDescription: UserProperties = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['getAll'],
			},
		},
		default: true,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['getAll'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'In Channel',
				name: 'inChannel',
				type: 'string',
				default: '',
				description: 'The ID of the channel to get users for',
			},
			{
				displayName: 'In Team',
				name: 'inTeam',
				type: 'string',
				default: '',
				description: 'The ID of the team to get users for',
			},
			{
				displayName: 'Not In Team',
				name: 'notInTeam',
				type: 'string',
				default: '',
				description: 'The ID of the team to exclude users for',
			},
			{
				displayName: 'Not In Channel',
				name: 'notInChannel',
				type: 'string',
				default: '',
				description: 'The ID of the channel to exclude users for',
			},
			{
				displayName: 'Sort',
				name: 'sort',
				type: 'options',
				options: [
					{
						name: 'Created At',
						value: 'createdAt',
					},
					{
						name: 'Last Activity At',
						value: 'lastActivityAt',
					},
					{
						name: 'Status',
						value: 'status',
					},
					{
						name: 'Username',
						value: 'username',
					},
				],
				default: 'username',
				description: 'The ID of the channel to exclude users for',
			},
		],
	},
];
