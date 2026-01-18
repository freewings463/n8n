"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Spotify/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Spotify 的节点。导入/依赖:外部:lodash/get；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:spotifyApiRequest、spotifyApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Spotify/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Spotify/GenericFunctions.py

import get from 'lodash/get';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	JsonObject,
	IHttpRequestMethods,
	IHttpRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to Spotify
 *
 */
export async function spotifyApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
	uri?: string,
): Promise<any> {
	const options: IHttpRequestOptions = {
		method,
		headers: {
			'User-Agent': 'n8n',
			'Content-Type': 'text/plain',
			Accept: ' application/json',
		},
		qs: query,
		url: uri ?? `https://api.spotify.com/v1${endpoint}`,
		json: true,
	};

	if (Object.keys(body).length > 0) {
		options.body = body;
	}
	try {
		return await this.helpers.httpRequestWithAuthentication.call(this, 'spotifyOAuth2Api', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function spotifyApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	let uri: string | undefined;

	do {
		responseData = await spotifyApiRequest.call(this, method, endpoint, body, query, uri);

		returnData.push.apply(returnData, get(responseData, propertyName));
		uri = responseData.next || responseData[propertyName.split('.')[0]].next;
		//remove the query as the query parameters are already included in the next, else api throws error.
		query = {};
		if (uri?.includes('offset=1000') && endpoint === '/search') {
			// The search endpoint has a limit of 1000 so step before it returns a 404
			return returnData;
		}
	} while (
		(responseData.next !== null && responseData.next !== undefined) ||
		(responseData[propertyName.split('.')[0]].next !== null &&
			responseData[propertyName.split('.')[0]].next !== undefined)
	);

	return returnData;
}
