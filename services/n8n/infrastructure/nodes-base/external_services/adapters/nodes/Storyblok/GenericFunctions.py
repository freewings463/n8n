"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Storyblok/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Storyblok 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:storyblokApiRequest、storyblokApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Storyblok/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Storyblok/GenericFunctions.py

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

export async function storyblokApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	option: IDataObject = {},
) {
	const authenticationMethod = this.getNodeParameter('source', 0) as string;

	let options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		qs,
		body,
		uri: '',
		json: true,
	};

	options = Object.assign({}, options, option);

	if (Object.keys(options.body).length === 0) {
		delete options.body;
	}

	if (authenticationMethod === 'contentApi') {
		const credentials = await this.getCredentials('storyblokContentApi');

		options.uri = `https://api.storyblok.com${resource}`;

		Object.assign(options.qs ?? {}, { token: credentials.apiKey });
	} else {
		const credentials = await this.getCredentials('storyblokManagementApi');

		options.uri = `https://mapi.storyblok.com${resource}`;

		if (options.headers) {
			Object.assign(options.headers, { Authorization: credentials.accessToken });
		}
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function storyblokApiRequestAllItems(
	this: IHookFunctions | ILoadOptionsFunctions | IExecuteFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;

	query.per_page = 100;

	query.page = 1;

	do {
		responseData = await storyblokApiRequest.call(this, method, resource, body, query);
		query.page++;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData[propertyName].length !== 0);

	return returnData;
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}
