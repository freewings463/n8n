"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:apiRequest、apiRequestAllItems、validateCredentials。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/transport/__init__.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	GenericValue,
	ICredentialDataDecryptedObject,
	ICredentialTestFunctions,
	IDataObject,
	IHttpRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to Mattermost
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'HEAD',
	endpoint: string,
	body: IDataObject | GenericValue | GenericValue[] = {},
	query: IDataObject = {},
) {
	const credentials = await this.getCredentials('syncroMspApi');

	query.api_key = credentials.apiKey;

	const options: IHttpRequestOptions = {
		method,
		body,
		qs: query,
		url: `https://${credentials.subdomain}.syncromsp.com/api/v1/${endpoint}`,
		headers: {},
	};

	try {
		return await this.helpers.httpRequest(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function apiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'HEAD',
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	let returnData: IDataObject[] = [];

	let responseData;
	query.page = 1;

	do {
		responseData = await apiRequest.call(this, method, endpoint, body, query);
		query.page++;
		returnData = returnData.concat(responseData[endpoint] as IDataObject[]);
	} while (responseData[endpoint].length !== 0);
	return returnData;
}

export async function validateCredentials(
	this: ICredentialTestFunctions,
	decryptedCredentials: ICredentialDataDecryptedObject,
): Promise<any> {
	const credentials = decryptedCredentials;

	const { subdomain, apiKey } = credentials as {
		subdomain: string;
		apiKey: string;
	};

	const options: IHttpRequestOptions = {
		method: 'GET',
		qs: {
			api_key: apiKey,
		},
		url: `https://${subdomain}.syncromsp.com/api/v1//me`,
	};

	return await this.helpers.request(options);
}
