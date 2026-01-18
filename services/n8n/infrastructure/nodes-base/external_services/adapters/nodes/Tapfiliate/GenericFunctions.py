"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Tapfiliate/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Tapfiliate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:tapfiliateApiRequest、tapfiliateApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Tapfiliate/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Tapfiliate/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function tapfiliateApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: IDataObject = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('tapfiliateApi');

	const options: IRequestOptions = {
		headers: {
			'Api-Key': credentials.apiKey,
		},
		method,
		qs,
		body,
		uri: uri || `https://api.tapfiliate.com/1.6${endpoint}`,
		json: true,
	};

	if (Object.keys(body).length === 0) {
		delete options.body;
	}

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function tapfiliateApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;

	query.page = 1;

	do {
		responseData = await tapfiliateApiRequest.call(this, method, endpoint, body, query, '', {
			resolveWithFullResponse: true,
		});
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
		query.page++;
	} while (responseData.headers.link.includes('next'));

	return returnData;
}
