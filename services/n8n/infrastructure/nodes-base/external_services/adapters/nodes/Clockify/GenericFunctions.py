"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clockify/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clockify 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:clockifyApiRequest、clockifyApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clockify/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clockify/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IPollFunctions,
	IDataObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

export async function clockifyApiRequest(
	this: ILoadOptionsFunctions | IPollFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	_uri?: string,
	_option: IDataObject = {},
): Promise<any> {
	const BASE_URL = 'https://api.clockify.me/api/v1';

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		qs,
		body,
		uri: `${BASE_URL}/${resource}`,
		json: true,
		useQuerystring: true,
	};
	return await this.helpers.requestWithAuthentication.call(this, 'clockifyApi', options);
}

export async function clockifyApiRequestAllItems(
	this: IExecuteFunctions | IPollFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query['page-size'] = 50;

	query.page = 1;

	do {
		responseData = await clockifyApiRequest.call(this, method, endpoint, body, query);

		returnData.push.apply(returnData, responseData as IDataObject[]);

		const limit = query.limit as number | undefined;
		if (limit && returnData.length >= limit) {
			return returnData;
		}

		query.page++;
	} while (responseData.length !== 0);

	return returnData;
}
