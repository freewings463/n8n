"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/VerticaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:VerticaApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/VerticaApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/VerticaApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class VerticaApi implements ICredentialType {
	name = 'verticaApi';

	displayName = 'Vertica API';

	documentationUrl = 'vertica';

	httpRequestNode = {
		name: 'Vertica',
		docsUrl: 'vertica',
		apiBaseUrlPlaceholder: 'http://<server>:<port>/v1/',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			required: true,
			type: 'string',
			default: 'https://localhost:8443',
			placeholder: 'https://<server>:<port>',
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
			default: '',
			description: 'The username for accessing the Vertica database.',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description: 'The password for accessing the Vertica database.',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			auth: {
				username: '={{$credentials.username}}',
				password: '={{$credentials.password}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}'.replace(/\/$/, ''),
			url: '/v1/health',
			method: 'GET',
			skipSslCertificateValidation: true,
		},
		rules: [
			{
				type: 'responseCode',
				properties: {
					value: 403,
					message: 'Connection failed: Invalid credentials or insufficient permissions',
				},
			},
			{
				type: 'responseCode',
				properties: {
					value: 503,
					message: 'Service unavailable: Server is overloaded or under maintenance',
				},
			},
			{
				type: 'responseCode',
				properties: {
					value: 504,
					message: 'Gateway timeout: Upstream server took too long to respond',
				},
			},
		],
	};
}
