"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/message/postEphemeral/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:messagePostEphemeralDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/message/postEphemeral/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/message/postEphemeral/description.py

import type { MessageProperties } from '../../Interfaces';

export const messagePostEphemeralDescription: MessageProperties = [
	{
		displayName: 'User Name or ID',
		name: 'userId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		options: [],
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['postEphemeral'],
				resource: ['message'],
			},
		},
		description:
			'ID of the user to send the ephemeral message to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Channel Name or ID',
		name: 'channelId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['postEphemeral'],
				resource: ['message'],
			},
		},
		description:
			'ID of the channel to send the ephemeral message in. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Message',
		name: 'message',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				operation: ['postEphemeral'],
				resource: ['message'],
			},
		},
		description: 'Text to send in the ephemeral message',
	},
];
