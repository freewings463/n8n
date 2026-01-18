"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/TheHiveApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:TheHiveApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/TheHiveApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/TheHiveApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class TheHiveApi implements ICredentialType {
	name = 'theHiveApi';

	displayName = 'The Hive API';

	documentationUrl = 'thehive';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'ApiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'URL',
			name: 'url',
			default: '',
			type: 'string',
			description: 'The URL of TheHive instance',
			placeholder: 'https://localhost:9000',
		},
		{
			displayName: 'API Version',
			name: 'apiVersion',
			default: '',
			type: 'options',
			description: 'The version of api to be used',
			options: [
				{
					name: 'TheHive 4+ (api v1)',
					value: 'v1',
					description:
						'API version with TheHive 4 support, also works with TheHive 5 but not all features are supported',
				},
				{
					name: 'TheHive 3 (api v0)',
					value: '',
					description: 'API version with TheHive 3 support',
				},
			],
		},
		{
			displayName: 'Ignore SSL Issues (Insecure)',
			name: 'allowUnauthorizedCerts',
			type: 'boolean',
			description: 'Whether to connect even if SSL certificate validation is not possible',
			default: false,
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials?.ApiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials?.url}}',
			url: '/api/case',
		},
	};
}
