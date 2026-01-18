"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./asset、./base、./Interfaces、./link 等1项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/router.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import * as asset from './asset';
import * as base from './base';
import type { SeaTable } from './Interfaces';
import * as link from './link';
import * as row from './row';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const operationResult: INodeExecutionData[] = [];
	let responseData: IDataObject | IDataObject[] = [];

	for (let i = 0; i < items.length; i++) {
		const resource = this.getNodeParameter<SeaTable>('resource', i);
		const operation = this.getNodeParameter('operation', i);

		const seatable = {
			resource,
			operation,
		} as SeaTable;

		try {
			if (seatable.resource === 'row') {
				responseData = await row[seatable.operation].execute.call(this, i);
			} else if (seatable.resource === 'base') {
				responseData = await base[seatable.operation].execute.call(this, i);
			} else if (seatable.resource === 'link') {
				responseData = await link[seatable.operation].execute.call(this, i);
			} else if (seatable.resource === 'asset') {
				responseData = await asset[seatable.operation].execute.call(this, i);
			}

			const executionData = this.helpers.constructExecutionMetaData(
				responseData as INodeExecutionData[],
				{
					itemData: { item: i },
				},
			);

			operationResult.push(...executionData);
		} catch (error) {
			if (this.continueOnFail()) {
				operationResult.push({ json: this.getInputData(i)[0].json, error });
			} else {
				if (error.context) error.context.itemIndex = i;
				throw error;
			}
		}
	}

	return [operationResult];
}
