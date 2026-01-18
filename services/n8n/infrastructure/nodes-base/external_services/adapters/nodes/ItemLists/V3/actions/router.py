"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ItemLists/V3/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ItemLists/V3 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./itemList、./node.type。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ItemLists/V3/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ItemLists/V3/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as itemList from './itemList';
import type { ItemListsType } from './node.type';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter<ItemListsType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const itemListsNodeData = {
		resource,
		operation,
	} as ItemListsType;

	switch (itemListsNodeData.resource) {
		case 'itemList':
			returnData = await itemList[itemListsNodeData.operation].execute.call(this, items);
			break;
		default:
			throw new NodeOperationError(
				this.getNode(),
				`The operation "${operation}" is not supported!`,
			);
	}

	return [returnData];
}
