"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Bitly/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Bitly 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:bitlyApiRequest、bitlyApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Bitly/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Bitly/GenericFunctions.py

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

export async function bitlyApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0) as string;
	let options: IRequestOptions = {
		headers: {},
		method,
		qs,
		body,
		uri: uri || `https://api-ssl.bitly.com/v4${resource}`,
		json: true,
	};
	options = Object.assign({}, options, option);
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}

	try {
		if (authenticationMethod === 'accessToken') {
			const credentials = await this.getCredentials('bitlyApi');
			options.headers = { Authorization: `Bearer ${credentials.accessToken}` };

			return await this.helpers.request(options);
		} else {
			return await this.helpers.requestOAuth2.call(this, 'bitlyOAuth2Api', options, {
				tokenType: 'Bearer',
			});
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an API request to paginated flow endpoint
 * and return all results
 */
export async function bitlyApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	let uri: string | undefined;
	query.size = 50;

	do {
		responseData = await bitlyApiRequest.call(this, method, resource, body, query, uri);
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		if (responseData.pagination?.next) {
			uri = responseData.pagination.next;
		}
	} while (responseData.pagination?.next !== undefined);
	return returnData;
}
