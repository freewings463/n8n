"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/CalendlyApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:CalendlyApi。关键函数/方法:getAuthenticationType、authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/CalendlyApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/CalendlyApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

const getAuthenticationType = (data: string): 'accessToken' | 'apiKey' => {
	// The access token is a JWT, so it will always include dots to separate
	// header, payoload and signature.
	return data.includes('.') ? 'accessToken' : 'apiKey';
};

export class CalendlyApi implements ICredentialType {
	name = 'calendlyApi';

	displayName = 'Calendly API';

	documentationUrl = 'calendly';

	properties: INodeProperties[] = [
		// Change name to Personal Access Token once API Keys
		// are deprecated
		{
			displayName: 'API Key or Personal Access Token',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		//check whether the token is an API Key or an access token
		const { apiKey } = credentials as { apiKey: string };
		const tokenType = getAuthenticationType(apiKey);
		// remove condition once v1 is deprecated
		// and only inject credentials as an access token
		if (tokenType === 'accessToken') {
			requestOptions.headers!.Authorization = `Bearer ${apiKey}`;
		} else {
			requestOptions.headers!['X-TOKEN'] = apiKey;
		}
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://calendly.com',
			url: '/api/v1/users/me',
		},
	};
}
