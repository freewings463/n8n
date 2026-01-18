"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/chatMessage/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./get.operation、./getAll.operation、./sendAndWait.operation。导出:create、get、getAll、sendAndWait、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/chatMessage/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/chatMessage/__init__.py

import { SEND_AND_WAIT_OPERATION, type INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as sendAndWait from './sendAndWait.operation';

export { create, get, getAll, sendAndWait };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['chatMessage'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a message in a chat',
				action: 'Create chat message',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a message from a chat',
				action: 'Get chat message',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many messages from a chat',
				action: 'Get many chat messages',
			},
			{
				name: 'Send and Wait for Response',
				value: SEND_AND_WAIT_OPERATION,
				description: 'Send a message and wait for response',
				action: 'Send message and wait for response',
			},
		],
		default: 'create',
	},

	...create.description,
	...get.description,
	...getAll.description,
	...sendAndWait.description,
];
