"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/Auth0ManagementApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:Auth0ManagementApi。关键函数/方法:preAuthentication。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/Auth0ManagementApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/Auth0ManagementApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestHelper,
	INodeProperties,
} from 'n8n-workflow';

export class Auth0ManagementApi implements ICredentialType {
	name = 'auth0ManagementApi';

	displayName = 'Auth0 Management API';

	documentationUrl = 'auth0management';

	icon = { light: 'file:icons/Auth0.svg', dark: 'file:icons/Auth0.dark.svg' } as const;

	httpRequestNode = {
		name: 'Auth0',
		docsUrl: 'https://auth0.com/docs/api/management/v2',
		apiBaseUrlPlaceholder: 'https://your-tenant.auth0.com/api/v2/users/',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Session Token',
			name: 'sessionToken',
			type: 'hidden',
			typeOptions: {
				expirable: true,
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Auth0 Domain',
			name: 'domain',
			type: 'string',
			required: true,
			default: 'your-domain.eu.auth0.com',
		},
		{
			displayName: 'Client ID',
			name: 'clientId',
			type: 'string',
			required: true,
			default: '',
		},
		{
			displayName: 'Client Secret',
			name: 'clientSecret',
			type: 'string',
			typeOptions: {
				password: true,
			},
			required: true,
			default: '',
		},
	];

	async preAuthentication(this: IHttpRequestHelper, credentials: ICredentialDataDecryptedObject) {
		const { access_token } = (await this.helpers.httpRequest({
			method: 'POST',
			url: `https://${credentials.domain}/oauth/token`,
			body: {
				client_id: credentials.clientId,
				client_secret: credentials.clientSecret,
				audience: `https://${credentials.domain}/api/v2/`,
				grant_type: 'client_credentials',
			},
			headers: {
				'Content-Type': 'application/json',
			},
		})) as { access_token: string };
		return { sessionToken: access_token };
	}

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.sessionToken}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '=https://{{$credentials.domain}}',
			url: '/api/v2/clients',
		},
	};
}
