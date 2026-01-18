"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Twilio/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Twilio 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:escapeXml。关键函数/方法:twilioApiRequest、twilioTriggerApiRequest、escapeXml。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Twilio/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Twilio/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	IHttpRequestMethods,
	IRequestOptions,
	IHttpRequestOptions,
	ILoadOptionsFunctions,
} from 'n8n-workflow';

/**
 * Make an API request to Twilio
 *
 */
export async function twilioApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	query?: IDataObject,
): Promise<any> {
	const credentials = await this.getCredentials<{
		accountSid: string;
		authType: 'authToken' | 'apiKey';
		authToken: string;
		apiKeySid: string;
		apiKeySecret: string;
	}>('twilioApi');

	if (query === undefined) {
		query = {};
	}

	const options: IRequestOptions = {
		method,
		form: body,
		qs: query,
		uri: `https://api.twilio.com/2010-04-01/Accounts/${credentials.accountSid}${endpoint}`,
		json: true,
	};

	return await this.helpers.requestWithAuthentication.call(this, 'twilioApi', options);
}

export async function twilioTriggerApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: FormData | IDataObject = {},
): Promise<any> {
	const options: IHttpRequestOptions = {
		method,
		body,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		url: `https://events.twilio.com/v1/${endpoint}`,
		json: true,
	};
	return await this.helpers.requestWithAuthentication.call(this, 'twilioApi', options);
}

const XML_CHAR_MAP: { [key: string]: string } = {
	'<': '&lt;',
	'>': '&gt;',
	'&': '&amp;',
	'"': '&quot;',
	"'": '&apos;',
};

export function escapeXml(str: string) {
	return str.replace(/[<>&"']/g, (ch: string) => {
		return XML_CHAR_MAP[ch];
	});
}
