"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/member/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./getAll.operation、./roleAdd.operation、./roleRemove.operation、../common.description。导出:getAll、roleAdd、roleRemove、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/member/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/member/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as getAll from './getAll.operation';
import * as roleAdd from './roleAdd.operation';
import * as roleRemove from './roleRemove.operation';
import { guildRLC } from '../common.description';

export { getAll, roleAdd, roleRemove };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['member'],
				authentication: ['botToken', 'oAuth2'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve the members of a server',
				action: 'Get many members',
			},
			{
				name: 'Role Add',
				value: 'roleAdd',
				description: 'Add a role to a member',
				action: 'Add a role to a member',
			},
			{
				name: 'Role Remove',
				value: 'roleRemove',
				description: 'Remove a role from a member',
				action: 'Remove a role from a member',
			},
		],
		default: 'getAll',
	},
	{
		...guildRLC,
		displayOptions: {
			show: {
				resource: ['member'],
				authentication: ['botToken', 'oAuth2'],
			},
		},
	},
	...getAll.description,
	...roleAdd.description,
	...roleRemove.description,
];
