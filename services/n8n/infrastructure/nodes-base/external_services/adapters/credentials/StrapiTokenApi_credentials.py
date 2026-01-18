"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/StrapiTokenApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:StrapiTokenApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/StrapiTokenApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/StrapiTokenApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class StrapiTokenApi implements ICredentialType {
	name = 'strapiTokenApi';

	displayName = 'Strapi API Token';

	documentationUrl = 'strapi';

	properties: INodeProperties[] = [
		{
			displayName: 'API Token',
			name: 'apiToken',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			default: '',
			placeholder: 'https://api.example.com',
		},
		{
			displayName: 'API Version',
			name: 'apiVersion',
			default: 'v3',
			type: 'options',
			description: 'The version of api to be used',
			options: [
				{
					name: 'Version 4',
					value: 'v4',
					description: 'API version supported by Strapi 4',
				},
				{
					name: 'Version 3',
					value: 'v3',
					description: 'API version supported by Strapi 3',
				},
			],
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiToken}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}',
			url: '={{$credentials.apiVersion === "v3" ? "/users/count" : "/api/users/count"}}',
			ignoreHttpStatusErrors: true,
		},
		rules: [
			{
				type: 'responseSuccessBody',
				properties: {
					key: 'error.name',
					value: 'UnauthorizedError',
					message: 'Invalid API token',
				},
			},
		],
	};
}
