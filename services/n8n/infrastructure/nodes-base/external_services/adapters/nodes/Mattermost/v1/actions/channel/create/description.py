"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/channel/create/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:channelCreateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/channel/create/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/channel/create/description.py

import type { ChannelProperties } from '../../Interfaces';

export const channelCreateDescription: ChannelProperties = [
	{
		displayName: 'Team Name or ID',
		name: 'teamId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		options: [],
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['channel'],
			},
		},
		description:
			'The Mattermost Team. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Display Name',
		name: 'displayName',
		type: 'string',
		default: '',
		placeholder: 'Announcements',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['channel'],
			},
		},
		required: true,
		description: 'The non-unique UI name for the channel',
	},
	{
		displayName: 'Name',
		name: 'channel',
		type: 'string',
		default: '',
		placeholder: 'announcements',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['channel'],
			},
		},
		required: true,
		description: 'The unique handle for the channel, will be present in the channel URL',
	},
	{
		displayName: 'Type',
		name: 'type',
		type: 'options',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['channel'],
			},
		},
		options: [
			{
				name: 'Private',
				value: 'private',
			},
			{
				name: 'Public',
				value: 'public',
			},
		],
		default: 'public',
		description: 'The type of channel to create',
	},
];
