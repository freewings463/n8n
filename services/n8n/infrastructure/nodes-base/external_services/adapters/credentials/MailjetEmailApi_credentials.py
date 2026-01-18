"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MailjetEmailApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:MailjetEmailApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MailjetEmailApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MailjetEmailApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class MailjetEmailApi implements ICredentialType {
	name = 'mailjetEmailApi';

	displayName = 'Mailjet Email API';

	documentationUrl = 'mailjet';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Secret Key',
			name: 'secretKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Sandbox Mode',
			name: 'sandboxMode',
			type: 'boolean',
			default: false,
			description:
				'Whether to allow to run the API call in a Sandbox mode, where all validations of the payload will be done without delivering the message',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			auth: {
				username: '={{$credentials.apiKey}}',
				password: '={{$credentials.secretKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.mailjet.com',
			url: '/v3/REST/template',
			method: 'GET',
		},
	};
}
