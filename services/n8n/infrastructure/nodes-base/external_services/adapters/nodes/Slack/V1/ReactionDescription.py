"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Slack/V1/ReactionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Slack/V1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:reactionOperations、reactionFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Slack/V1/ReactionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Slack/V1/ReactionDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const reactionOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['reaction'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Adds a reaction to a message',
				action: 'Add a reaction',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get the reactions of a message',
				action: 'Get a reaction',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a reaction of a message',
				action: 'Remove a reaction',
			},
		],
		default: 'add',
	},
];

export const reactionFields: INodeProperties[] = [
	{
		displayName: 'Channel Name or ID',
		name: 'channelId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['reaction'],
				operation: ['add', 'get', 'remove'],
			},
		},
		description:
			'Channel containing the message. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Emoji',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['reaction'],
				operation: ['add', 'remove'],
			},
		},
		description: 'Name of emoji',
		placeholder: '+1',
	},
	{
		displayName: 'Timestamp',
		name: 'timestamp',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['reaction'],
				operation: ['add', 'get', 'remove'],
			},
		},
		description: 'Timestamp of the message',
	},
];
