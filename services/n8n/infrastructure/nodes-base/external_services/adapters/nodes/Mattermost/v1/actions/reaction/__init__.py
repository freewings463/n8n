"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/reaction/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create、./del、./getAll。导出:create、del、getAll、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/reaction/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/reaction/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create';
import * as del from './del';
import * as getAll from './getAll';

export { create, del as delete, getAll };

export const descriptions: INodeProperties[] = [
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
				name: 'Create',
				value: 'create',
				description: 'Add a reaction to a post',
				action: 'Create a reaction',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Remove a reaction from a post',
				action: 'Delete a reaction',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many reactions to one or more posts',
				action: 'Get many reactions',
			},
		],
		default: 'create',
	},
	...create.description,
	...del.description,
	...getAll.description,
];
