"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:apiRequest、baseUrl、apiRequestAllItems。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/transport/__init__.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	GenericValue,
	IDataObject,
	IHttpRequestMethods,
	IHttpRequestOptions,
} from 'n8n-workflow';

/**
 * Make an API request to Mattermost
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject | GenericValue | GenericValue[] = {},
	query: IDataObject = {},
) {
	const credentials = await this.getCredentials('mattermostApi');
	const baseUrl = (credentials.baseUrl as string).replace(/\/$/, '');

	const options: IHttpRequestOptions = {
		method,
		body,
		qs: query,
		url: `${baseUrl}/api/v4/${endpoint}`,
		headers: {
			'content-type': 'application/json; charset=utf-8',
		},
		skipSslCertificateValidation: credentials.allowUnauthorizedCerts as boolean,
	};

	return await this.helpers.httpRequestWithAuthentication.call(this, 'mattermostApi', options);
}

export async function apiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'HEAD',
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;
	query.page = 0;
	query.per_page = 100;

	do {
		responseData = await apiRequest.call(this, method, endpoint, body, query);
		query.page++;
		returnData.push.apply(returnData, responseData as IDataObject[]);
	} while (responseData.length !== 0);

	return returnData;
}
