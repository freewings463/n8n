"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Reddit/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Reddit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:redditApiRequest、redditApiRequestAllItems、handleListing。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Reddit/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Reddit/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an authenticated or unauthenticated API request to Reddit.
 */
export async function redditApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject,
): Promise<any> {
	const resource = this.getNodeParameter('resource', 0) as string;

	const authRequired = ['profile', 'post', 'postComment'].includes(resource);

	qs.api_type = 'json';

	const options: IRequestOptions = {
		headers: {
			'user-agent': 'n8n',
		},
		method,
		uri: authRequired
			? `https://oauth.reddit.com/${endpoint}`
			: `https://www.reddit.com/${endpoint}`,
		qs,
		json: true,
	};

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	if (authRequired) {
		try {
			return await this.helpers.requestOAuth2.call(this, 'redditOAuth2Api', options);
		} catch (error) {
			throw new NodeApiError(this.getNode(), error as JsonObject);
		}
	} else {
		try {
			return await this.helpers.request.call(this, options);
		} catch (error) {
			throw new NodeApiError(this.getNode(), error as JsonObject);
		}
	}
}

/**
 * Make an unauthenticated API request to Reddit and return all results.
 */
export async function redditApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject,
): Promise<any> {
	let responseData;
	const returnData: IDataObject[] = [];

	const resource = this.getNodeParameter('resource', 0);
	const operation = this.getNodeParameter('operation', 0);
	const returnAll = this.getNodeParameter('returnAll', 0, false) as boolean;

	qs.limit = 100;

	do {
		responseData = await redditApiRequest.call(this, method, endpoint, qs);
		if (!Array.isArray(responseData)) {
			qs.after = responseData.data.after;
		}

		if (endpoint === 'api/search_subreddits.json') {
			responseData.subreddits.forEach((child: any) => returnData.push(child as IDataObject));
		} else if (resource === 'postComment' && operation === 'getAll') {
			responseData[1].data.children.forEach((child: any) =>
				returnData.push(child.data as IDataObject),
			);
		} else {
			responseData.data.children.forEach((child: any) =>
				returnData.push(child.data as IDataObject),
			);
		}
		if (qs.limit && returnData.length >= qs.limit && !returnAll) {
			return returnData;
		}
	} while (responseData.data?.after);

	return returnData;
}

/**
 * Handles a large Reddit listing by returning all items or up to a limit.
 */
export async function handleListing(
	this: IExecuteFunctions,
	i: number,
	endpoint: string,
	qs: IDataObject = {},
	requestMethod: 'GET' | 'POST' = 'GET',
): Promise<any> {
	let responseData;

	const returnAll = this.getNodeParameter('returnAll', i);

	if (returnAll) {
		responseData = await redditApiRequestAllItems.call(this, requestMethod, endpoint, qs);
	} else {
		const limit = this.getNodeParameter('limit', i);
		qs.limit = limit;
		responseData = await redditApiRequestAllItems.call(this, requestMethod, endpoint, qs);
		responseData = responseData.slice(0, limit);
	}

	return responseData;
}
