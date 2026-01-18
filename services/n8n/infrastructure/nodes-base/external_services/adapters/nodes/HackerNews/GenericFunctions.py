"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HackerNews/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HackerNews 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:hackerNewsApiRequest、hackerNewsApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HackerNews/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HackerNews/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to HackerNews
 *
 */
export async function hackerNewsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject,
): Promise<any> {
	const options: IRequestOptions = {
		method,
		qs,
		uri: `http://hn.algolia.com/api/v1/${endpoint}`,
		json: true,
	};

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an API request to HackerNews
 * and return all results
 *
 * @param {(IHookFunctions | IExecuteFunctions)} this
 */
export async function hackerNewsApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject,
): Promise<any> {
	qs.hitsPerPage = 100;

	const returnData: IDataObject[] = [];

	let responseData;
	let itemsReceived = 0;

	do {
		responseData = await hackerNewsApiRequest.call(this, method, endpoint, qs);
		returnData.push.apply(returnData, responseData.hits as IDataObject[]);

		if (returnData !== undefined) {
			itemsReceived += returnData.length;
		}
	} while (responseData.nbHits > itemsReceived);

	return returnData;
}
