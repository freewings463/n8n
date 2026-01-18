"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/channelMessage/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./getAll.operation。导出:create、getAll、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/channelMessage/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/channelMessage/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as getAll from './getAll.operation';

export { create, getAll };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['channelMessage'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a message in a channel',
				action: 'Create message',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many messages from a channel',
				action: 'Get many messages',
			},
		],
		default: 'create',
	},

	...create.description,
	...getAll.description,
];
