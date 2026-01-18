"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PagerDuty/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PagerDuty 的节点。导入/依赖:外部:change-case；内部:n8n-workflow；本地:无。导出:keysToSnakeCase。关键函数/方法:pagerDutyApiRequest、pagerDutyApiRequestAllItems、keysToSnakeCase。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PagerDuty/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PagerDuty/GenericFunctions.py

import { snakeCase } from 'change-case';
import type {
	JsonObject,
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IHookFunctions,
	IWebhookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function pagerDutyApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
	uri?: string,
	headers: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	const options: IRequestOptions = {
		headers: {
			Accept: 'application/vnd.pagerduty+json;version=2',
		},
		method,
		body,
		qs: query,
		uri: uri || `https://api.pagerduty.com${resource}`,
		json: true,
		qsStringifyOptions: {
			arrayFormat: 'brackets',
		},
	};

	if (!Object.keys(body as IDataObject).length) {
		delete options.form;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}

	options.headers = Object.assign({}, options.headers, headers);

	try {
		if (authenticationMethod === 'apiToken') {
			const credentials = await this.getCredentials('pagerDutyApi');

			options.headers.Authorization = `Token token=${credentials.apiToken}`;

			return await this.helpers.request(options);
		} else {
			return await this.helpers.requestOAuth2.call(this, 'pagerDutyOAuth2Api', options);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function pagerDutyApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	query.limit = 100;
	query.offset = 0;

	do {
		responseData = await pagerDutyApiRequest.call(this, method, endpoint, body, query);
		query.offset++;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData.more);

	return returnData;
}

export function keysToSnakeCase(elements: IDataObject[] | IDataObject): IDataObject[] {
	if (!Array.isArray(elements)) {
		elements = [elements];
	}
	for (const element of elements) {
		for (const key of Object.keys(element)) {
			if (key !== snakeCase(key)) {
				element[snakeCase(key)] = element[key];
				delete element[key];
			}
		}
	}
	return elements;
}
