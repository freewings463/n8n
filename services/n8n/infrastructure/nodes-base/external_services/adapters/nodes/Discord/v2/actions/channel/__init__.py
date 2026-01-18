"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/channel/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteChannel.operation、./get.operation、./getAll.operation 等2项。导出:create、get、getAll、update、deleteChannel、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/channel/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/channel/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteChannel from './deleteChannel.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as update from './update.operation';
import { guildRLC } from '../common.description';

export { create, get, getAll, update, deleteChannel };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['channel'],
				authentication: ['botToken', 'oAuth2'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new channel',
				action: 'Create a channel',
			},
			{
				name: 'Delete',
				value: 'deleteChannel',
				description: 'Delete a channel',
				action: 'Delete a channel',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a channel',
				action: 'Get a channel',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve the channels of a server',
				action: 'Get many channels',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a channel',
				action: 'Update a channel',
			},
		],
		default: 'create',
	},
	{
		...guildRLC,
		displayOptions: {
			show: {
				resource: ['channel'],
				authentication: ['botToken', 'oAuth2'],
			},
		},
	},
	...create.description,
	...deleteChannel.description,
	...get.description,
	...getAll.description,
	...update.description,
];
