"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Webflow/V2/actions/Item/Item.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Webflow/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./get.operation、./getAll.operation 等1项。导出:create、deleteItem、get、getAll、update、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Webflow/V2/actions/Item/Item.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Webflow/V2/actions/Item/Item_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteItem from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as update from './update.operation';

export { create, deleteItem, get, getAll, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create an item',
			},
			{
				name: 'Delete',
				value: 'deleteItem',
				action: 'Delete an item',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an item',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many items',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update an item',
			},
		],
		displayOptions: {
			show: {
				resource: ['item'],
			},
		},
	},
	...create.description,
	...deleteItem.description,
	...get.description,
	...getAll.description,
	...update.description,
];
