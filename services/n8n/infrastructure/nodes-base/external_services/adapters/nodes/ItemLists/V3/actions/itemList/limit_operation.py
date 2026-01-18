"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ItemLists/V3/actions/itemList/limit.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ItemLists/V3 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:无。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ItemLists/V3/actions/itemList/limit.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ItemLists/V3/actions/itemList/limit_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

const properties: INodeProperties[] = [
	{
		displayName: 'Max Items',
		name: 'maxItems',
		type: 'number',
		typeOptions: {
			minValue: 1,
		},
		default: 1,
		description: 'If there are more items than this number, some are removed',
	},
	{
		displayName: 'Keep',
		name: 'keep',
		type: 'options',
		options: [
			{
				name: 'First Items',
				value: 'firstItems',
			},
			{
				name: 'Last Items',
				value: 'lastItems',
			},
		],
		default: 'firstItems',
		description: 'When removing items, whether to keep the ones at the start or the ending',
	},
];

const displayOptions = {
	show: {
		resource: ['itemList'],
		operation: ['limit'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
): Promise<INodeExecutionData[]> {
	let returnData = items;
	const maxItems = this.getNodeParameter('maxItems', 0) as number;
	const keep = this.getNodeParameter('keep', 0) as string;

	if (maxItems > items.length) {
		return returnData;
	}

	if (keep === 'firstItems') {
		returnData = items.slice(0, maxItems);
	} else {
		returnData = items.slice(items.length - maxItems, items.length);
	}
	return returnData;
}
