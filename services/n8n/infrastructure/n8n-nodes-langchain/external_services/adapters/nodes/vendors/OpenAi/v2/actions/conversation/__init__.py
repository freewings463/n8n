"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/conversation/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./get.operation、./remove.operation、./update.operation。导出:create、get、remove、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/conversation/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/conversation/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as get from './get.operation';
import * as remove from './remove.operation';
import * as update from './update.operation';

export { create, get, remove, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a conversation',
				description: 'Create a conversation',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a conversation',
				description: 'Get a conversation',
			},
			{
				name: 'Remove',
				value: 'remove',
				action: 'Remove a conversation',
				description: 'Remove a conversation',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a conversation',
				description: 'Update a conversation',
			},
		],
		default: 'create',
		displayOptions: {
			show: {
				resource: ['conversation'],
			},
		},
	},
	...create.description,
	...remove.description,
	...update.description,
	...get.description,
];
