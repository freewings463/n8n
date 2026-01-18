"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Bubble/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Bubble 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:bubbleApiRequest、bubbleApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Bubble/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Bubble/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an authenticated API request to Bubble.
 */
export async function bubbleApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	qs: IDataObject,
) {
	const { apiToken, appName, domain, environment, hosting } = await this.getCredentials<{
		apiToken: string;
		appName: string;
		domain: string;
		environment: 'development' | 'live';
		hosting: 'bubbleHosted' | 'selfHosted';
	}>('bubbleApi');

	const rootUrl = hosting === 'bubbleHosted' ? `https://${appName}.bubbleapps.io` : domain;
	const urlSegment = environment === 'development' ? '/version-test/api/1.1' : '/api/1.1';

	const options: IRequestOptions = {
		headers: {
			'user-agent': 'n8n',
			Authorization: `Bearer ${apiToken}`,
		},
		method,
		uri: `${rootUrl}${urlSegment}${endpoint}`,
		qs,
		body,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an authenticated API request to Bubble and return all results.
 */
export async function bubbleApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	qs: IDataObject,
) {
	const returnData: IDataObject[] = [];

	let responseData;
	qs.limit = 100;
	qs.cursor = 0;
	do {
		responseData = await bubbleApiRequest.call(this, method, endpoint, body, qs);
		qs.cursor += qs.limit;
		returnData.push.apply(returnData, responseData.response.results as IDataObject[]);
	} while (responseData.response.remaining !== 0);

	return returnData;
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}
