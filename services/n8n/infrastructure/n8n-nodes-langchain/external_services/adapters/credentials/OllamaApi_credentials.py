"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/OllamaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:OllamaApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/OllamaApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/OllamaApi_credentials.py

import type {
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
	IAuthenticateGeneric,
} from 'n8n-workflow';

export class OllamaApi implements ICredentialType {
	name = 'ollamaApi';

	displayName = 'Ollama';

	documentationUrl = 'ollama';

	properties: INodeProperties[] = [
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			required: true,
			type: 'string',
			default: 'http://localhost:11434',
		},
		{
			displayName: 'API Key',
			hint: 'When using Ollama behind a proxy with authentication (such as Open WebUI), provide the Bearer token/API key here. This is not required for the default Ollama installation',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: false,
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{ $credentials.baseUrl }}',
			url: '/api/tags',
			method: 'GET',
		},
	};
}
