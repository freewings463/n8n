"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/customer/update/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:updateCustomer。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/customer/update/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/customer/update/execute.py

import type { IDataObject, IExecuteFunctions, INodeExecutionData, JsonObject } from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function updateCustomer(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const id = this.getNodeParameter('customerId', index) as IDataObject;
	const {
		address,
		businessName,
		email,
		firstName,
		getSms,
		invoiceCcEmails,
		lastName,
		noEmail,
		notes,
		notificationEmail,
		phone,
		referredBy,
	} = this.getNodeParameter('updateFields', index);

	const qs = {} as IDataObject;
	const requestMethod = 'PUT';
	const endpoint = `customers/${id}`;
	let body = {} as IDataObject;
	let addressData = address as IDataObject;

	if (addressData) {
		addressData = addressData.addressFields as IDataObject;
		addressData.address_2 = addressData.address2;
	}

	body = {
		...addressData,
		business_name: businessName,
		email,
		firstname: firstName,
		get_sms: getSms,
		invoice_cc_emails: ((invoiceCcEmails as string[]) || []).join(','),
		lastname: lastName,
		no_email: noEmail,
		notes,
		notification_email: notificationEmail,
		phone,
		referred_by: referredBy,
	};

	const responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);
	if (!responseData.customer) {
		throw new NodeApiError(this.getNode(), responseData as JsonObject, {
			httpCode: '404',
			message: 'Customer ID not found',
		});
	}
	return this.helpers.returnJsonArray(responseData.customer as IDataObject[]);
}
