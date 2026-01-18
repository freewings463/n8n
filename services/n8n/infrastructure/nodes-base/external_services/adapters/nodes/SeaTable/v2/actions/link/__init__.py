"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/link/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./add.operation、./list.operation、./remove.operation。导出:add、list、remove、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/link/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/link/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as add from './add.operation';
import * as list from './list.operation';
import * as remove from './remove.operation';

export { add, list, remove };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['link'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Create a link between two rows in a link column',
				action: 'Add a row link',
			},
			{
				name: 'List',
				value: 'list',
				description: 'List all links of a specific row',
				action: 'List row links',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a link between two rows from a link column',
				action: 'Remove a row link',
			},
		],
		default: 'add',
	},
	...add.description,
	...list.description,
	...remove.description,
];
