"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/page/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deletePage.operation、./search.operation、./update.operation。导出:create、deletePage、search、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/page/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/page/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deletePage from './deletePage.operation';
import * as search from './search.operation';
import * as update from './update.operation';

export { create, deletePage, search, update };

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
				name: 'Create',
				value: 'create',
				action: 'Create a page',
			},
			{
				name: 'Delete',
				value: 'deletePage',
				action: 'Delete a page',
			},
			{
				name: 'Search',
				value: 'search',
				action: 'Search pages',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a page',
			},
		],
		displayOptions: {
			show: {
				resource: ['page'],
			},
		},
	},
	...create.description,
	...deletePage.description,
	...search.description,
	...update.description,
];
