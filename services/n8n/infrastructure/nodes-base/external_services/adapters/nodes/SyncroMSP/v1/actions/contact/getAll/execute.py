"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/contact/getAll/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:getAll。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/contact/getAll/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/contact/getAll/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { apiRequest, apiRequestAllItems } from '../../../transport';

export async function getAll(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const returnAll = this.getNodeParameter('returnAll', index);

	const qs = {} as IDataObject;
	const requestMethod = 'GET';
	const endpoint = 'contacts';
	const body = {} as IDataObject;

	let responseData;
	if (returnAll) {
		responseData = await apiRequestAllItems.call(this, requestMethod, endpoint, body, qs);
		return this.helpers.returnJsonArray(responseData);
	} else {
		const limit = this.getNodeParameter('limit', index);
		responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);
		return this.helpers.returnJsonArray(responseData.contacts.splice(0, limit) as IDataObject[]);
	}
}
