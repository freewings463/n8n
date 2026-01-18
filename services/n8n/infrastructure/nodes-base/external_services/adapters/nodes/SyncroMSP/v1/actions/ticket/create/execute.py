"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/ticket/create/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:createTicket。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/ticket/create/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/ticket/create/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function createTicket(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const id = this.getNodeParameter('customerId', index) as IDataObject;
	const subject = this.getNodeParameter('subject', index) as IDataObject;
	const { assetId, issueType, status, contactId } = this.getNodeParameter(
		'additionalFields',
		index,
	);

	const qs = {} as IDataObject;
	const requestMethod = 'POST';
	const endpoint = 'tickets';
	let body = {} as IDataObject;

	body = {
		asset_id: assetId,
		//due_date: dueDate,
		problem_type: issueType,
		status,
		contact_id: contactId,
	};

	body.customer_id = id;
	body.subject = subject;

	const responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);

	return this.helpers.returnJsonArray(responseData.ticket as IDataObject[]);
}
