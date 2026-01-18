"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/TwilioApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:TwilioApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/TwilioApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/TwilioApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties } from 'n8n-workflow';

export class TwilioApi implements ICredentialType {
	name = 'twilioApi';

	displayName = 'Twilio API';

	documentationUrl = 'twilio';

	properties: INodeProperties[] = [
		{
			displayName: 'Auth Type',
			name: 'authType',
			type: 'options',
			default: 'authToken',
			options: [
				{
					name: 'Auth Token',
					value: 'authToken',
				},
				{
					name: 'API Key',
					value: 'apiKey',
				},
			],
		},
		{
			displayName: 'Account SID',
			name: 'accountSid',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Auth Token',
			name: 'authToken',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			displayOptions: {
				show: {
					authType: ['authToken'],
				},
			},
		},
		{
			displayName: 'API Key SID',
			name: 'apiKeySid',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			displayOptions: {
				show: {
					authType: ['apiKey'],
				},
			},
		},
		{
			displayName: 'API Key Secret',
			name: 'apiKeySecret',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			displayOptions: {
				show: {
					authType: ['apiKey'],
				},
			},
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			auth: {
				username:
					'={{ $credentials.authType === "apiKey" ? $credentials.apiKeySid : $credentials.accountSid }}',
				password:
					'={{ $credentials.authType === "apiKey" ? $credentials.apiKeySecret : $credentials.authToken }}',
			},
		},
	};
}
