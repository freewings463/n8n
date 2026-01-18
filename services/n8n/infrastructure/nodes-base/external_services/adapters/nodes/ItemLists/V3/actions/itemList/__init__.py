"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ItemLists/V3/actions/itemList/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ItemLists/V3 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./concatenateItems.operation、./limit.operation、./removeDuplicates.operation、./sort.operation 等2项。导出:concatenateItems、limit、removeDuplicates、sort、splitOutItems、summarize、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ItemLists/V3/actions/itemList/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ItemLists/V3/actions/itemList/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as concatenateItems from './concatenateItems.operation';
import * as limit from './limit.operation';
import * as removeDuplicates from './removeDuplicates.operation';
import * as sort from './sort.operation';
import * as splitOutItems from './splitOutItems.operation';
import * as summarize from './summarize.operation';

export { concatenateItems, limit, removeDuplicates, sort, splitOutItems, summarize };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['itemList'],
			},
		},
		options: [
			{
				name: 'Concatenate Items',
				value: 'concatenateItems',
				description: 'Combine fields into a list in a single new item',
				action: 'Concatenate Items',
			},
			{
				name: 'Limit',
				value: 'limit',
				description: 'Remove items if there are too many',
				action: 'Limit',
			},
			{
				name: 'Remove Duplicates',
				value: 'removeDuplicates',
				description: 'Remove extra items that are similar',
				action: 'Remove Duplicates',
			},
			{
				name: 'Sort',
				value: 'sort',
				description: 'Change the item order',
				action: 'Sort',
			},
			{
				name: 'Split Out Items',
				value: 'splitOutItems',
				description:
					"Turn a list or values of object's properties inside item(s) into separate items",
				action: 'Split Out Items',
			},
			{
				name: 'Summarize',
				value: 'summarize',
				description: 'Aggregate items together (pivot table)',
				action: 'Summarize',
			},
		],
		default: 'splitOutItems',
	},
	...concatenateItems.description,
	...limit.description,
	...removeDuplicates.description,
	...sort.description,
	...splitOutItems.description,
	...summarize.description,
];
