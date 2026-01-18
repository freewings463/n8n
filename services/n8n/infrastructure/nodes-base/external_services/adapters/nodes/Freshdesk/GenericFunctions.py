"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshdesk/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshdesk 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON、capitalize。关键函数/方法:freshdeskApiRequest、freshdeskApiRequestAllItems、validateJSON、capitalize。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshdesk/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshdesk/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { BINARY_ENCODING, NodeApiError } from 'n8n-workflow';

export async function freshdeskApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('freshdeskApi');

	const apiKey = `${credentials.apiKey}:X`;

	const endpoint = 'freshdesk.com/api/v2';

	let options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
			Authorization: `${Buffer.from(apiKey).toString(BINARY_ENCODING)}`,
		},
		method,
		body,
		qs: query,
		uri: uri || `https://${credentials.domain}.${endpoint}${resource}`,
		json: true,
	};
	if (!Object.keys(body as IDataObject).length) {
		delete options.body;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}
	options = Object.assign({}, options, option);
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function freshdeskApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;
	let uri: string | undefined;
	query.per_page = 100;
	do {
		responseData = await freshdeskApiRequest.call(this, method, endpoint, body, query, uri, {
			resolveWithFullResponse: true,
		});
		if (responseData.headers.link) {
			uri = responseData.headers.link.split(';')[0].replace('<', '').replace('>', '');
		}
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
	} while (responseData.headers.link?.includes('rel="next"'));
	return returnData;
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = [];
	}
	return result;
}

export function capitalize(s: string): string {
	if (typeof s !== 'string') return '';
	return s.charAt(0).toUpperCase() + s.slice(1);
}
