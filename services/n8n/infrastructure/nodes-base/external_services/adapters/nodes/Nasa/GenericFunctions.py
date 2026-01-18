"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Nasa/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Nasa 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:nasaApiRequest、nasaApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Nasa/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Nasa/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function nasaApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject,
	option: IDataObject = {},
	uri?: string,
): Promise<any> {
	const credentials = await this.getCredentials('nasaApi');

	qs.api_key = credentials.api_key as string;

	const options: IRequestOptions = {
		method,
		qs,
		uri: uri || `https://api.nasa.gov${endpoint}`,
		json: true,
	};

	if (Object.keys(option)) {
		Object.assign(options, option);
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function nasaApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	resource: string,
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query.size = 20;

	let uri: string | undefined = undefined;

	do {
		responseData = await nasaApiRequest.call(this, method, resource, query, {}, uri);
		uri = responseData.links.next;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData.links.next !== undefined);

	return returnData;
}
