"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/Limit/Limit.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/Limit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Limit。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/Limit/Limit.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Transform/Limit/Limit_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

export class Limit implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Limit',
		name: 'limit',
		icon: 'file:limit.svg',
		group: ['transform'],
		subtitle: '',
		version: 1,
		description: 'Restrict the number of items',
		defaults: {
			name: 'Limit',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
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
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		let returnData = items;
		const maxItems = this.getNodeParameter('maxItems', 0) as number;
		const keep = this.getNodeParameter('keep', 0) as string;

		if (maxItems > items.length) {
			return [returnData];
		}

		if (keep === 'firstItems') {
			returnData = items.slice(0, maxItems);
		} else {
			returnData = items.slice(items.length - maxItems, items.length);
		}
		return [returnData];
	}
}
