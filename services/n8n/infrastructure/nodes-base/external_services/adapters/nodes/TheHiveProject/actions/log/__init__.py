"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/log/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./addAttachment.operation、./create.operation、./deleteAttachment.operation、./deleteLog.operation 等3项。导出:addAttachment、create、deleteAttachment、deleteLog、executeResponder、get、search、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/log/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/log/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as addAttachment from './addAttachment.operation';
import * as create from './create.operation';
import * as deleteAttachment from './deleteAttachment.operation';
import * as deleteLog from './deleteLog.operation';
import * as executeResponder from './executeResponder.operation';
import * as get from './get.operation';
import * as search from './search.operation';

export { addAttachment, create, deleteAttachment, deleteLog, executeResponder, get, search };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		noDataExpression: true,
		type: 'options',
		required: true,
		default: 'create',
		options: [
			{
				name: 'Add Attachment',
				value: 'addAttachment',
				action: 'Add attachment to a task log',
			},
			{
				name: 'Create',
				value: 'create',
				action: 'Create a task log',
			},
			{
				name: 'Delete',
				value: 'deleteLog',
				action: 'Delete task log',
			},
			{
				name: 'Delete Attachment',
				value: 'deleteAttachment',
				action: 'Delete attachment from a task log',
			},
			{
				name: 'Execute Responder',
				value: 'executeResponder',
				action: 'Execute responder on a task log',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a task log',
			},
			{
				name: 'Search',
				value: 'search',
				action: 'Search task logs',
			},
		],
		displayOptions: {
			show: {
				resource: ['log'],
			},
		},
	},
	...addAttachment.description,
	...create.description,
	...deleteAttachment.description,
	...deleteLog.description,
	...executeResponder.description,
	...get.description,
	...search.description,
];
