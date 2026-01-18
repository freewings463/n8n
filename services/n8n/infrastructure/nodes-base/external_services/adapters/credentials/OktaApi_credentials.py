"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/OktaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:OktaApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/OktaApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/OktaApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class OktaApi implements ICredentialType {
	name = 'oktaApi';

	displayName = 'Okta API';

	documentationUrl = 'okta';

	icon = { light: 'file:icons/Okta.svg', dark: 'file:icons/Okta.dark.svg' } as const;

	httpRequestNode = {
		name: 'Okta',
		docsUrl: 'https://developer.okta.com/docs/reference/',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			required: true,
			default: '',
			placeholder: 'https://dev-123456.okta.com',
		},
		{
			displayName: 'Access Token',
			name: 'accessToken',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
			description: 'Secure Session Web Service Access Token',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=SSWS {{$credentials.accessToken}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}',
			url: '/api/v1/api-tokens',
		},
	};
}
