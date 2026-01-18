"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./contact、./customer、./Interfaces、./rmm 等1项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/router.py

import type { IExecuteFunctions, INodeExecutionData, JsonObject } from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import * as contact from './contact';
import * as customer from './customer';
import type { SyncroMsp } from './Interfaces';
import * as rmm from './rmm';
import * as ticket from './ticket';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const operationResult: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		const resource = this.getNodeParameter<SyncroMsp>('resource', i);
		let operation = this.getNodeParameter('operation', i);
		let responseData: INodeExecutionData[] = [];
		if (operation === 'del') {
			operation = 'delete';
		}

		const syncroMsp = {
			resource,
			operation,
		} as SyncroMsp;

		try {
			if (syncroMsp.resource === 'customer') {
				responseData = await customer[syncroMsp.operation].execute.call(this, i);
			} else if (syncroMsp.resource === 'ticket') {
				responseData = await ticket[syncroMsp.operation].execute.call(this, i);
			} else if (syncroMsp.resource === 'contact') {
				responseData = await contact[syncroMsp.operation].execute.call(this, i);
			} else if (syncroMsp.resource === 'rmm') {
				responseData = await rmm[syncroMsp.operation].execute.call(this, i);
			}

			const executionData = this.helpers.constructExecutionMetaData(responseData, {
				itemData: { item: i },
			});

			operationResult.push(...executionData);
		} catch (err) {
			if (this.continueOnFail()) {
				const executionErrorData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray({ error: err.message }),
					{ itemData: { item: i } },
				);
				operationResult.push(...executionErrorData);
			} else {
				throw new NodeApiError(this.getNode(), err as JsonObject, { itemIndex: i });
			}
		}
	}

	return [operationResult];
}
