"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Elastic/ElasticSecurity/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Elastic/ElasticSecurity 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./types。导出:tolerateTrailingSlash、throwOnEmptyUpdate。关键函数/方法:tolerateTrailingSlash、elasticSecurityApiRequest、elasticSecurityApiRequestAllItems、handleListing、getConnector、throwOnEmptyUpdate、getVersion。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Elastic/ElasticSecurity/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Elastic/ElasticSecurity/GenericFunctions.py

import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import type { Connector, ElasticSecurityApiCredentials } from './types';

export function tolerateTrailingSlash(baseUrl: string) {
	return baseUrl.endsWith('/') ? baseUrl.substr(0, baseUrl.length - 1) : baseUrl;
}

export async function elasticSecurityApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const { baseUrl: rawBaseUrl } =
		await this.getCredentials<ElasticSecurityApiCredentials>('elasticSecurityApi');

	const baseUrl = tolerateTrailingSlash(rawBaseUrl);

	const options: IRequestOptions = {
		method,
		body,
		qs,
		uri: `${baseUrl}/api${endpoint}`,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.requestWithAuthentication.call(this, 'elasticSecurityApi', options);
	} catch (error) {
		if (error?.error?.error === 'Not Acceptable' && error?.error?.message) {
			error.error.error = `${error.error.error}: ${error.error.message}`;
		}

		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function elasticSecurityApiRequestAllItems(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	let _page = 1;
	const returnData: IDataObject[] = [];
	let responseData: any;

	const resource = this.getNodeParameter('resource', 0) as 'case' | 'caseComment';

	do {
		responseData = await elasticSecurityApiRequest.call(this, method, endpoint, body, qs);
		_page++;

		const items = resource === 'case' ? responseData.cases : responseData;

		returnData.push(...(items as IDataObject[]));
	} while (returnData.length < responseData.total);

	return returnData;
}

export async function handleListing(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const returnAll = this.getNodeParameter('returnAll', 0);

	if (returnAll) {
		return await elasticSecurityApiRequestAllItems.call(this, method, endpoint, body, qs);
	}

	const responseData = await elasticSecurityApiRequestAllItems.call(
		this,
		method,
		endpoint,
		body,
		qs,
	);
	const limit = this.getNodeParameter('limit', 0);

	return responseData.slice(0, limit);
}

/**
 * Retrieve a connector name and type from a connector ID.
 *
 * https://www.elastic.co/guide/en/kibana/master/get-connector-api.html
 */
export async function getConnector(this: IExecuteFunctions, connectorId: string) {
	const endpoint = `/actions/connector/${connectorId}`;
	const {
		id,
		name,
		connector_type_id: type,
	} = (await elasticSecurityApiRequest.call(this, 'GET', endpoint)) as Connector;

	return { id, name, type };
}

export function throwOnEmptyUpdate(this: IExecuteFunctions, resource: string) {
	throw new NodeOperationError(
		this.getNode(),
		`Please enter at least one field to update for the ${resource}`,
	);
}

export async function getVersion(this: IExecuteFunctions, endpoint: string) {
	const { version } = (await elasticSecurityApiRequest.call(this, 'GET', endpoint)) as {
		version?: string;
	};

	if (!version) {
		throw new NodeOperationError(this.getNode(), 'Cannot retrieve version for resource');
	}

	return version;
}
