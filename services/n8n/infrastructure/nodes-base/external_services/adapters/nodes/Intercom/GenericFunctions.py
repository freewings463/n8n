"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Intercom/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Intercom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:intercomApiRequest、intercomApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Intercom/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Intercom/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IHttpRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function intercomApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	endpoint: string,
	method: IHttpRequestMethods,

	body: any = {},
	query?: IDataObject,
	uri?: string,
): Promise<any> {
	const options: IHttpRequestOptions = {
		method,
		qs: query,
		url: uri ?? `https://api.intercom.io${endpoint}`,
		body,
		json: true,
	};

	try {
		return await this.helpers.httpRequestWithAuthentication.call(this, 'intercomApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an API request to paginated intercom endpoint
 * and return all results
 */
export async function intercomApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	propertyName: string,
	endpoint: string,
	method: IHttpRequestMethods,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query.per_page = 60;

	let uri: string | undefined;

	do {
		responseData = await intercomApiRequest.call(this, endpoint, method, body, query, uri);
		uri = responseData.pages.next;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData.pages?.next !== null);

	return returnData;
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = '';
	}
	return result;
}
