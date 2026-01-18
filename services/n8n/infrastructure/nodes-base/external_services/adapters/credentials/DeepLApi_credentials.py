"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/DeepLApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:DeepLApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/DeepLApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/DeepLApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class DeepLApi implements ICredentialType {
	name = 'deepLApi';

	displayName = 'DeepL API';

	documentationUrl = 'deepl';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'API Plan',
			name: 'apiPlan',
			type: 'options',
			options: [
				{
					name: 'Pro Plan',
					value: 'pro',
				},
				{
					name: 'Free Plan',
					value: 'free',
				},
			],
			default: 'pro',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			qs: {
				auth_key: '={{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL:
				'={{$credentials.apiPlan === "pro" ? "https://api.deepl.com/v2" : "https://api-free.deepl.com/v2" }}',
			url: '/usage',
		},
	};
}
