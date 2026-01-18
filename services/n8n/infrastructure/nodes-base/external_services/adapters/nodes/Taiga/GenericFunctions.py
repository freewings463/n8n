"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Taiga/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Taiga 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./types。导出:getAutomaticSecret、toOptions、throwOnEmptyUpdate。关键函数/方法:getAuthorization、taigaApiRequest、taigaApiRequestAllItems、getAutomaticSecret、handleListing、toOptions、throwOnEmptyUpdate、getVersionForUpdate。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Taiga/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Taiga/GenericFunctions.py

import { createHash } from 'crypto';
import type {
	ICredentialDataDecryptedObject,
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';
import type { LoadedResource, Resource } from './types';

export async function getAuthorization(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	credentials?: ICredentialDataDecryptedObject,
): Promise<string> {
	if (credentials === undefined) {
		throw new NodeOperationError(this.getNode(), 'No credentials got returned!');
	}

	const { password, username } = credentials;
	const options: IRequestOptions = {
		headers: { 'Content-Type': 'application/json' },
		method: 'POST',
		body: {
			type: 'normal',
			password,
			username,
		},
		uri: credentials.url ? `${credentials.url}/api/v1/auth` : 'https://api.taiga.io/api/v1/auth',
		json: true,
	};

	try {
		const response = await this.helpers.request(options);

		return response.auth_token;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function taigaApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body = {},
	query = {},
	uri?: string,
	option = {},
): Promise<any> {
	const credentials = await this.getCredentials('taigaApi');

	const authToken = await getAuthorization.call(this, credentials);

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		auth: {
			bearer: authToken,
		},
		qs: query,
		method,
		body,
		uri:
			uri || credentials.url
				? `${credentials.url}/api/v1${resource}`
				: `https://api.taiga.io/api/v1${resource}`,
		json: true,
	};

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function taigaApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: IDataObject = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	let uri: string | undefined;

	do {
		responseData = await taigaApiRequest.call(this, method, resource, body, query, uri, {
			resolveWithFullResponse: true,
		});
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
		uri = responseData.headers['x-pagination-next'];
		const limit = query.limit as number | undefined;
		if (limit && returnData.length >= limit) {
			return returnData;
		}
	} while (
		responseData.headers['x-pagination-next'] !== undefined &&
		responseData.headers['x-pagination-next'] !== ''
	);
	return returnData;
}

export function getAutomaticSecret(credentials: ICredentialDataDecryptedObject) {
	const data = `${credentials.username},${credentials.password}`;
	return createHash('md5').update(data).digest('hex');
}

export async function handleListing(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	qs: IDataObject,
	i: number,
) {
	let responseData;
	qs.project = this.getNodeParameter('projectId', i) as number;
	const returnAll = this.getNodeParameter('returnAll', i);

	if (returnAll) {
		return await taigaApiRequestAllItems.call(this, method, endpoint, body, qs);
	} else {
		qs.limit = this.getNodeParameter('limit', i);
		responseData = await taigaApiRequestAllItems.call(this, method, endpoint, body, qs);
		return responseData.splice(0, qs.limit);
	}
}

export const toOptions = (items: LoadedResource[]) =>
	items.map(({ name, id }) => ({ name, value: id }));

export function throwOnEmptyUpdate(this: IExecuteFunctions, resource: Resource) {
	throw new NodeOperationError(
		this.getNode(),
		`Please enter at least one field to update for the ${resource}.`,
	);
}

export async function getVersionForUpdate(this: IExecuteFunctions, endpoint: string) {
	return await taigaApiRequest.call(this, 'GET', endpoint).then((response) => response.version);
}
