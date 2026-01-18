"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Calendly/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Calendly 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:getAuthenticationTypeFromApiKey、getAuthenticationType、calendlyApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Calendly/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Calendly/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IHookFunctions,
	IWebhookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

function getAuthenticationTypeFromApiKey(data: string): 'accessToken' | 'apiKey' {
	// The access token is a JWT, so it will always include dots to separate
	// header, payoload and signature.
	return data.includes('.') ? 'accessToken' : 'apiKey';
}

export async function getAuthenticationType(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
): Promise<'accessToken' | 'apiKey'> {
	const authentication = this.getNodeParameter('authentication', 0) as string;
	if (authentication === 'apiKey') {
		const { apiKey } = await this.getCredentials<{ apiKey: string }>('calendlyApi');
		return getAuthenticationTypeFromApiKey(apiKey);
	} else {
		return 'accessToken';
	}
}

export async function calendlyApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const authenticationType = await getAuthenticationType.call(this);

	const headers: IDataObject = {
		'Content-Type': 'application/json',
	};

	let endpoint = 'https://api.calendly.com';

	// remove once API key is deprecated
	if (authenticationType === 'apiKey') {
		endpoint = 'https://calendly.com/api/v1';
	}

	let options: IRequestOptions = {
		headers,
		method,
		body,
		qs: query,
		uri: uri || `${endpoint}${resource}`,
		json: true,
	};

	if (!Object.keys(body as IDataObject).length) {
		delete options.form;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}
	options = Object.assign({}, options, option);

	const credentialsType =
		(this.getNodeParameter('authentication', 0) as string) === 'apiKey'
			? 'calendlyApi'
			: 'calendlyOAuth2Api';
	return await this.helpers.requestWithAuthentication.call(this, credentialsType, options);
}
