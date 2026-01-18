"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Beeminder/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Beeminder 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:isValidAuthenticationMethod、beeminderApiRequest、beeminderApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Beeminder/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Beeminder/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHookFunctions,
	IWebhookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { ApplicationError } from 'n8n-workflow';

const BEEMINDER_URI = 'https://www.beeminder.com/api/v1';

function isValidAuthenticationMethod(value: unknown): value is 'apiToken' | 'oAuth2' {
	return typeof value === 'string' && ['apiToken', 'oAuth2'].includes(value);
}

export async function beeminderApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0, 'apiToken');

	if (!isValidAuthenticationMethod(authenticationMethod)) {
		throw new ApplicationError(`Invalid authentication method: ${authenticationMethod}`);
	}

	let credentialType = 'beeminderApi';
	if (authenticationMethod === 'oAuth2') {
		credentialType = 'beeminderOAuth2Api';
	}

	const options: IRequestOptions = {
		method,
		body,
		qs: query,
		uri: `${BEEMINDER_URI}${endpoint}`,
		json: true,
	};

	if (!Object.keys(body as IDataObject).length) {
		delete options.body;
	}

	if (!Object.keys(query).length) {
		delete options.qs;
	}

	return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
}

export async function beeminderApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions | IHookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	query.page = 1;
	do {
		responseData = await beeminderApiRequest.call(this, method, endpoint, body, query);
		query.page++;
		returnData.push.apply(returnData, responseData as IDataObject[]);
	} while (responseData.length !== 0);

	return returnData;
}
