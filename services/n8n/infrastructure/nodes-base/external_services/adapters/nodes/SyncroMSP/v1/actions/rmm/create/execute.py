"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/rmm/create/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:addAlert。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/rmm/create/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/rmm/create/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function addAlert(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const customerId = this.getNodeParameter('customerId', index) as IDataObject;
	const assetId = this.getNodeParameter('assetId', index) as IDataObject;
	const description = this.getNodeParameter('description', index) as IDataObject;
	const additionalFields = this.getNodeParameter('additionalFields', index);

	const qs = {} as IDataObject;
	const requestMethod = 'POST';
	const endpoint = 'rmm_alerts';
	let body = {} as IDataObject;

	if (additionalFields) {
		body = additionalFields;
	}

	body.customer_id = customerId;
	body.asset_id = assetId;
	body.description = description;

	const responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);

	return this.helpers.returnJsonArray(responseData.alert as IDataObject);
}
