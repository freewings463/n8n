"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/CertificateManager/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/CertificateManager 的节点。导入/依赖:外部:lodash/get；内部:n8n-workflow；本地:../GenericFunctions。导出:无。关键函数/方法:awsApiRequest、awsApiRequestREST、awsApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/CertificateManager/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/CertificateManager/GenericFunctions.py

import get from 'lodash/get';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IHttpRequestOptions,
	JsonObject,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { jsonParse, NodeApiError } from 'n8n-workflow';
import { getAwsCredentials } from '../GenericFunctions';

export async function awsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer,
	query: IDataObject = {},
	headers?: object,
): Promise<any> {
	const { credentials, credentialsType } = await getAwsCredentials(this);

	const requestOptions = {
		qs: {
			service,
			path,
			...query,
		},
		headers,
		method,
		url: '',
		body,
		region: credentials?.region as string,
	} as IHttpRequestOptions;

	try {
		return await this.helpers.requestWithAuthentication.call(this, credentialsType, requestOptions);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function awsApiRequestREST(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	query: IDataObject = {},
	headers?: object,
): Promise<any> {
	const response = await awsApiRequest.call(this, service, method, path, body, query, headers);
	try {
		return JSON.parse(response as string);
	} catch (e) {
		return response;
	}
}

export async function awsApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	query: IDataObject = {},
	headers: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await awsApiRequestREST.call(this, service, method, path, body, query, headers);
		if (responseData.NextToken) {
			const data = jsonParse<any>(body as string, {
				errorMessage: 'Response body is not valid JSON',
			});
			data.NextToken = responseData.NextToken;
		}
		returnData.push.apply(returnData, get(responseData, propertyName) as IDataObject[]);
	} while (responseData.NextToken !== undefined);

	return returnData;
}
