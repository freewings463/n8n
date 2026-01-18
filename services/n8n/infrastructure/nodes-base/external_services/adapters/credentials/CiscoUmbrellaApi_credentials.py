"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/CiscoUmbrellaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:CiscoUmbrellaApi。关键函数/方法:preAuthentication。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/CiscoUmbrellaApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/CiscoUmbrellaApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestHelper,
	INodeProperties,
} from 'n8n-workflow';

export class CiscoUmbrellaApi implements ICredentialType {
	name = 'ciscoUmbrellaApi';

	displayName = 'Cisco Umbrella API';

	documentationUrl = 'ciscoumbrella';

	icon = { light: 'file:icons/Cisco.svg', dark: 'file:icons/Cisco.dark.svg' } as const;

	httpRequestNode = {
		name: 'Cisco Umbrella',
		docsUrl: 'https://developer.cisco.com/docs/cloud-security/',
		apiBaseUrl: 'https://api.umbrella.com/',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Session Token',
			name: 'sessionToken',
			type: 'hidden',

			typeOptions: {
				expirable: true,
			},
			default: '',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
		},
		{
			displayName: 'Secret',
			name: 'secret',
			type: 'string',
			typeOptions: {
				password: true,
			},
			required: true,
			default: '',
		},
	];

	async preAuthentication(this: IHttpRequestHelper, credentials: ICredentialDataDecryptedObject) {
		const url = 'https://api.umbrella.com';
		const { access_token } = (await this.helpers.httpRequest({
			method: 'POST',
			url: `${
				url.endsWith('/') ? url.slice(0, -1) : url
			}/auth/v2/token?grant_type=client_credentials`,
			auth: {
				username: credentials.apiKey as string,
				password: credentials.secret as string,
			},
			headers: {
				'Content-Type': 'x-www-form-urlencoded',
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
			baseURL: 'https://api.umbrella.com',
			url: '/users',
		},
	};
}
