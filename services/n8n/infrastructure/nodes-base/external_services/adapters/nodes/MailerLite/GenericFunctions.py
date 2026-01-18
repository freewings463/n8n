"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MailerLite/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MailerLite 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v2/MailerLite.Interface。导出:无。关键函数/方法:mailerliteApiRequest、mailerliteApiRequestAllItems、getCustomFields、fields。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MailerLite/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MailerLite/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	INodePropertyOptions,
	JsonObject,
	IHttpRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import type { CustomField } from './v2/MailerLite.Interface';

export async function mailerliteApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions | IHookFunctions,
	method: IHttpRequestMethods,
	path: string,
	body: any = {},
	qs: IDataObject = {},
	_option = {},
): Promise<any> {
	const options: IHttpRequestOptions = {
		method,
		body,
		qs,
		url:
			this.getNode().typeVersion === 1
				? `https://api.mailerlite.com/api/v2${path}`
				: `https://connect.mailerlite.com/api${path}`,
		json: true,
	};
	try {
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}

		return await this.helpers.httpRequestWithAuthentication.call(this, 'mailerLiteApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function mailerliteApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions | IHookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];
	let responseData;

	query.limit = 1000;
	query.offset = 0;

	if (this.getNode().typeVersion === 1) {
		do {
			responseData = await mailerliteApiRequest.call(this, method, endpoint, body, query);
			returnData.push(...(responseData as IDataObject[]));
			query.offset += query.limit;
		} while (responseData.length !== 0);
	} else {
		do {
			responseData = await mailerliteApiRequest.call(this, method, endpoint, body, query);
			returnData.push(...(responseData.data as IDataObject[]));
			query.cursor = responseData.meta.next_cursor;
		} while (responseData.links.next !== null);
	}

	return returnData;
}

export async function getCustomFields(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const endpoint = '/fields';
	const fieldsResponse = await mailerliteApiRequest.call(this, 'GET', endpoint);

	if (this.getNode().typeVersion === 1) {
		const fields = fieldsResponse as CustomField[];
		fields.forEach((field) => {
			returnData.push({
				name: field.key,
				value: field.key,
			});
		});
	} else {
		const fields = (fieldsResponse as IDataObject).data as CustomField[];
		fields.forEach((field) => {
			returnData.push({
				name: field.name,
				value: field.key,
			});
		});
	}

	return returnData;
}
