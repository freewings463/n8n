"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/CopperApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:CopperApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/CopperApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/CopperApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class CopperApi implements ICredentialType {
	name = 'copperApi';

	displayName = 'Copper API';

	documentationUrl = 'copper';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Email',
			name: 'email',
			required: true,
			type: 'string',
			placeholder: 'name@email.com',
			default: '',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'X-PW-AccessToken': '={{$credentials.apiKey}}',
				'X-PW-Application': 'developer_api',
				'X-PW-UserEmail': '={{$credentials.email}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.copper.com/developer_api/v1/',
			url: 'users/me',
		},
	};
}
