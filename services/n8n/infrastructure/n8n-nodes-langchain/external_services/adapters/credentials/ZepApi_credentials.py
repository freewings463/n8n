"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/ZepApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ZepApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/ZepApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/ZepApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class ZepApi implements ICredentialType {
	name = 'zepApi';

	displayName = 'Zep Api';

	documentationUrl = 'zep';

	properties: INodeProperties[] = [
		{
			displayName: 'This Zep integration is deprecated and will be removed in a future version.',
			name: 'deprecationNotice',
			type: 'notice',
			default: '',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: false,
			default: '',
		},
		{
			displayName: 'Cloud',
			description: 'Whether you are adding credentials for Zep Cloud instead of Zep Open Source',
			name: 'cloud',
			type: 'boolean',
			default: false,
		},
		{
			displayName: 'API URL',
			name: 'apiUrl',
			required: false,
			type: 'string',
			default: 'http://localhost:8000',
			displayOptions: {
				show: {
					cloud: [false],
				},
			},
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization:
					'={{$credentials.apiKey && !$credentials.cloud ? "Bearer " + $credentials.apiKey : "Api-Key " + $credentials.apiKey }}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{!$credentials.cloud ? $credentials.apiUrl : "https://api.getzep.com"}}',
			url: '={{!$credentials.cloud ? "/api/v1/collection" : "/api/v2/collections"}}',
		},
	};
}
