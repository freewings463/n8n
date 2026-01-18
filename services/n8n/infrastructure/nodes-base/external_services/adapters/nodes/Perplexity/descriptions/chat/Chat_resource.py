"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Perplexity/descriptions/chat/Chat.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Perplexity/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./complete.operation、../../GenericFunctions。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Perplexity/descriptions/chat/Chat.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Perplexity/descriptions/chat/Chat_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as complete from './complete.operation';
import { sendErrorPostReceive } from '../../GenericFunctions';

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['chat'],
			},
		},
		options: [
			{
				name: 'Message a Model',
				value: 'complete',
				action: 'Message a model',
				description: 'Create one or more completions for a given text',
				routing: {
					request: {
						method: 'POST',
						url: '/chat/completions',
					},
					output: {
						postReceive: [sendErrorPostReceive],
					},
				},
			},
		],
		default: 'complete',
	},

	...complete.description,
];
