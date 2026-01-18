"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/ticket/update/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:updateTicket。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/ticket/update/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/ticket/update/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function updateTicket(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const id = this.getNodeParameter('ticketId', index) as IDataObject;
	const { assetId, customerId, dueDate, issueType, status, subject, ticketType, contactId } =
		this.getNodeParameter('updateFields', index);

	const qs = {} as IDataObject;
	const requestMethod = 'PUT';
	const endpoint = `tickets/${id}`;
	let body = {} as IDataObject;

	body = {
		...(assetId && { asset_id: assetId }),
		...(customerId && { customer_id: customerId }),
		...(dueDate && { due_date: dueDate }),
		...(issueType && { problem_type: issueType }),
		...(status && { status }),
		...(subject && { subject }),
		...(ticketType && { ticket_type: ticketType }),
		...(contactId && { contact_id: contactId }),
	};

	if (!Object.keys(body).length) {
		throw new NodeOperationError(this.getNode(), 'At least one update fields has to be defined', {
			itemIndex: index,
		});
	}

	const responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);

	return this.helpers.returnJsonArray(responseData.ticket as IDataObject[]);
}
