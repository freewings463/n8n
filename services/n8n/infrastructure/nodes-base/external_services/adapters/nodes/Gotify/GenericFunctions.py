"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Gotify/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Gotify 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:gotifyApiRequest、gotifyApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Gotify/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Gotify/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function gotifyApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	path: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	_option = {},
): Promise<any> {
	const credentials = await this.getCredentials('gotifyApi');

	const options: IRequestOptions = {
		method,
		headers: {
			'X-Gotify-Key': method === 'POST' ? credentials.appApiToken : credentials.clientApiToken,
			accept: 'application/json',
		},
		body,
		qs,
		uri: uri || `${credentials.url}${path}`,
		json: true,
		rejectUnauthorized: !credentials.ignoreSSLIssues,
	};
	try {
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}

		return await this.helpers.request.call(this, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function gotifyApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	let uri: string | undefined;
	query.limit = 100;
	do {
		responseData = await gotifyApiRequest.call(this, method, endpoint, body, query, uri);
		if (responseData.paging.next) {
			uri = responseData.paging.next;
		}
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData.paging.next);

	return returnData;
}
