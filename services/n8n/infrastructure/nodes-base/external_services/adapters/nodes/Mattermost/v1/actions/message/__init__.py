"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/message/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./del、./post、./postEphemeral。导出:del、post、postEphemeral、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/message/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/message/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as del from './del';
import * as post from './post';
import * as postEphemeral from './postEphemeral';

export { del as delete, post, postEphemeral };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['message'],
			},
		},
		options: [
			{
				name: 'Delete',
				value: 'delete',
				description: 'Soft delete a post, by marking the post as deleted in the database',
				action: 'Delete a message',
			},
			{
				name: 'Post',
				value: 'post',
				description: 'Post a message into a channel',
				action: 'Post a message',
			},
			{
				name: 'Post Ephemeral',
				value: 'postEphemeral',
				description: 'Post an ephemeral message into a channel',
				action: 'Post an ephemeral message',
			},
		],
		default: 'post',
	},
	...del.description,
	...post.description,
	...postEphemeral.description,
];
