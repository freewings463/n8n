"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/assistant/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteAssistant.operation、./list.operation、./message.operation 等1项。导出:create、deleteAssistant、message、list、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/assistant/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/assistant/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteAssistant from './deleteAssistant.operation';
import * as list from './list.operation';
import * as message from './message.operation';
import * as update from './update.operation';

export { create, deleteAssistant, message, list, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Create an Assistant',
				value: 'create',
				action: 'Create an assistant',
				description: 'Create a new assistant',
			},
			{
				name: 'Delete an Assistant',
				value: 'deleteAssistant',
				action: 'Delete an assistant',
				description: 'Delete an assistant from the account',
			},
			{
				name: 'List Assistants',
				value: 'list',
				action: 'List assistants',
				description: 'List assistants in the organization',
			},
			{
				name: 'Message an Assistant',
				value: 'message',
				action: 'Message an assistant',
				description: 'Send messages to an assistant',
			},
			{
				name: 'Update an Assistant',
				value: 'update',
				action: 'Update an assistant',
				description: 'Update an existing assistant',
			},
		],
		default: 'message',
		displayOptions: {
			show: {
				resource: ['assistant'],
			},
		},
	},

	...create.description,
	...deleteAssistant.description,
	...message.description,
	...list.description,
	...update.description,
];
