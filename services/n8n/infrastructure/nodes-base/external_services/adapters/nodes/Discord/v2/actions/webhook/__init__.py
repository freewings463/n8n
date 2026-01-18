"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/webhook/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的Webhook入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./sendLegacy.operation。导出:sendLegacy、description。关键函数/方法:无。用于汇总导出并完成Webhook模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/webhook/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/webhook/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as sendLegacy from './sendLegacy.operation';

export { sendLegacy };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				authentication: ['webhook'],
			},
		},
		options: [
			{
				name: 'Send a Message',
				value: 'sendLegacy',
				description: 'Send a message to a channel using the webhook',
				action: 'Send a message',
			},
		],
		default: 'sendLegacy',
	},
	...sendLegacy.description,
];
