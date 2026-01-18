"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Trello/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Trello 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:apiRequest、apiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Trello/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Trello/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

/**
 * Make an API request to Trello
 *
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
): Promise<any> {
	query = query || {};

	const options: IRequestOptions = {
		method,
		body,
		qs: query,
		uri: `https://api.trello.com/1/${endpoint}`,
		json: true,
	};

	if (method === 'GET') {
		delete options.body;
	}

	return await this.helpers.requestWithAuthentication.call(this, 'trelloApi', options);
}

export async function apiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	query: IDataObject = {},
): Promise<any> {
	query.limit = 30;

	query.sort = '-id';

	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await apiRequest.call(this, method, endpoint, body, query);
		returnData.push.apply(returnData, responseData as IDataObject[]);
		if (responseData.length !== 0) {
			query.before = responseData[responseData.length - 1].id;
		}
	} while (query.limit <= responseData.length);

	return returnData;
}
