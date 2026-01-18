"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SurveyMonkey/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SurveyMonkey 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:idsExist。关键函数/方法:surveyMonkeyApiRequest、surveyMonkeyRequestAllItems、idsExist。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SurveyMonkey/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SurveyMonkey/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHookFunctions,
	IWebhookFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function surveyMonkeyApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: IDataObject = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	const endpoint = 'https://api.surveymonkey.com/v3';

	let options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs: query,
		uri: uri || `${endpoint}${resource}`,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}
	options = Object.assign({}, options, option);

	try {
		if (authenticationMethod === 'accessToken') {
			const credentials = await this.getCredentials('surveyMonkeyApi');

			(options.headers as IDataObject).Authorization = `bearer ${credentials.accessToken}`;

			return await this.helpers.request(options);
		} else {
			return await this.helpers.requestOAuth2?.call(this, 'surveyMonkeyOAuth2Api', options);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function surveyMonkeyRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,

	body: IDataObject = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	query.page = 1;
	query.per_page = 100;
	let uri: string | undefined;

	do {
		responseData = await surveyMonkeyApiRequest.call(this, method, endpoint, body, query, uri);
		uri = responseData.links.next;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData.links.next);

	return returnData;
}

export function idsExist(ids: string[], surveyIds: string[]) {
	for (const surveyId of surveyIds) {
		if (!ids.includes(surveyId)) {
			return false;
		}
	}
	return true;
}
