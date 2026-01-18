"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/channel/search/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:channelSearchDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/channel/search/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/channel/search/description.py

import type { ChannelProperties } from '../../Interfaces';

export const channelSearchDescription: ChannelProperties = [
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
				operation: ['search'],
				resource: ['channel'],
			},
		},
		description:
			'The Mattermost Team. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Search Term',
		name: 'term',
		type: 'string',
		default: '',
		placeholder: 'General',
		displayOptions: {
			show: {
				operation: ['search'],
				resource: ['channel'],
			},
		},
		required: true,
		description: 'The search term for Channels in a Team',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				operation: ['search'],
				resource: ['channel'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 100,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		displayOptions: {
			show: {
				operation: ['search'],
				resource: ['channel'],
				returnAll: [false],
			},
		},
	},
];
