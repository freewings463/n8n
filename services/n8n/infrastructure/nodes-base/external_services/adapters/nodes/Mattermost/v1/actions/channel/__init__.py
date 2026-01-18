"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/channel/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./addUser、./create、./del、./members 等3项。导出:create、del、members、restore、addUser、statistics、search、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/channel/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/channel/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as addUser from './addUser';
import * as create from './create';
import * as del from './del';
import * as members from './members';
import * as restore from './restore';
import * as search from './search';
import * as statistics from './statistics';

export { create, del as delete, members, restore, addUser, statistics, search };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['channel'],
			},
		},
		options: [
			{
				name: 'Add User',
				value: 'addUser',
				description: 'Add a user to a channel',
				action: 'Add a user to a channel',
			},
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new channel',
				action: 'Create a channel',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Soft delete a channel',
				action: 'Delete a channel',
			},
			{
				name: 'Member',
				value: 'members',
				description: 'Get a page of members for a channel',
				action: 'Get a page of members for a channel',
			},
			{
				name: 'Restore',
				value: 'restore',
				description: 'Restores a soft deleted channel',
				action: 'Restore a soft-deleted channel',
			},
			{
				name: 'Search',
				value: 'search',
				description: 'Search for a channel',
				action: 'Search for a channel',
			},
			{
				name: 'Statistics',
				value: 'statistics',
				description: 'Get statistics for a channel',
				action: 'Get statistics for a channel',
			},
		],
		default: 'create',
	},
	...create.description,
	...del.description,
	...members.description,
	...restore.description,
	...addUser.description,
	...statistics.description,
	...search.description,
];
