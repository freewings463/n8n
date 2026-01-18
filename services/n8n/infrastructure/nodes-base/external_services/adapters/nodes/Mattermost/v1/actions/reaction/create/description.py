"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/reaction/create/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:reactionCreateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/reaction/create/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/reaction/create/description.py

import type { ReactionProperties } from '../../Interfaces';

export const reactionCreateDescription: ReactionProperties = [
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
				resource: ['reaction'],
				operation: ['create'],
			},
		},
		description:
			'ID of the user sending the reaction. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Post ID',
		name: 'postId',
		type: 'string',
		default: '',
		placeholder: '3moacfqxmbdw38r38fjprh6zsr',
		required: true,
		displayOptions: {
			show: {
				resource: ['reaction'],
				operation: ['create'],
			},
		},
		description:
			'ID of the post to react to. Obtainable from the post link: <code>https://mattermost.internal.n8n.io/[server]/pl/[postId]</code>',
	},
	{
		displayName: 'Emoji Name',
		name: 'emojiName',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['reaction'],
				operation: ['create'],
			},
		},
		description: 'Emoji to use for this reaction',
	},
];
