"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wordpress/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wordpress 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:wordpressApiRequest、wordpressApiRequestAllItems、parseInt。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wordpress/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wordpress/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function wordpressApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('wordpressApi');

	let options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			'User-Agent': 'n8n',
		},
		method,
		qs,
		body,
		uri: uri || `${credentials.url}/wp-json/wp/v2${resource}`,
		rejectUnauthorized: !credentials.allowUnauthorizedCerts,
		json: true,
	};
	options = Object.assign({}, options, option);
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}
	try {
		const credentialType = 'wordpressApi';
		return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function wordpressApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query.per_page = 10;
	query.page = 0;

	do {
		query.page++;
		responseData = await wordpressApiRequest.call(this, method, endpoint, body, query, undefined, {
			resolveWithFullResponse: true,
		});
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
	} while (
		responseData.headers['x-wp-totalpages'] !== undefined &&
		responseData.headers['x-wp-totalpages'] !== '0' &&
		parseInt(responseData.headers['x-wp-totalpages'] as string, 10) !== query.page
	);

	return returnData;
}
