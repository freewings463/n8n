"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TravisCi/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TravisCi 的节点。导入/依赖:外部:lodash/get；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:travisciApiRequest、travisciApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TravisCi/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TravisCi/GenericFunctions.py

import get from 'lodash/get';
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

export async function travisciApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject | string = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('travisCiApi');
	let options: IRequestOptions = {
		headers: {
			'Travis-API-Version': '3',
			Accept: 'application/json',
			'Content-Type': 'application.json',
			Authorization: `token ${credentials.apiToken}`,
		},
		method,
		qs,
		body,
		uri: uri || `https://api.travis-ci.com${resource}`,
		json: true,
	};
	options = Object.assign({}, options, option);
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an API request to paginated TravisCI endpoint
 * and return all results
 */
export async function travisciApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	resource: string,

	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await travisciApiRequest.call(this, method, resource, body, query);
		const path = get(responseData, '@pagination.next.@href') as string;
		if (path !== undefined) {
			const parsedPath = new URLSearchParams(path);
			query = Object.fromEntries(parsedPath);
		}
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData['@pagination'].is_last !== true);
	return returnData;
}
