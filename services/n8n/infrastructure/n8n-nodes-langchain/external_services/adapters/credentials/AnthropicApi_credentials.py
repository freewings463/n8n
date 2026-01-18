"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/AnthropicApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:AnthropicApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/AnthropicApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/AnthropicApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class AnthropicApi implements ICredentialType {
	name = 'anthropicApi';

	displayName = 'Anthropic';

	documentationUrl = 'anthropic';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
		},
		{
			displayName: 'Base URL',
			name: 'url',
			type: 'string',
			default: 'https://api.anthropic.com',
			description: 'Override the default base URL for the API',
		},
		{
			displayName: 'Add Custom Header',
			name: 'header',
			type: 'boolean',
			default: false,
		},
		{
			displayName: 'Header Name',
			name: 'headerName',
			type: 'string',
			displayOptions: {
				show: {
					header: [true],
				},
			},
			default: '',
		},
		{
			displayName: 'Header Value',
			name: 'headerValue',
			type: 'string',
			typeOptions: {
				password: true,
			},
			displayOptions: {
				show: {
					header: [true],
				},
			},
			default: '',
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials?.url}}',
			url: '/v1/messages',
			method: 'POST',
			headers: {
				'anthropic-version': '2023-06-01',
			},
			body: {
				model: 'claude-3-haiku-20240307',
				messages: [{ role: 'user', content: 'Hey' }],
				max_tokens: 1,
			},
		},
	};

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		requestOptions.headers ??= {};

		requestOptions.headers['x-api-key'] = credentials.apiKey;

		if (
			credentials.header &&
			typeof credentials.headerName === 'string' &&
			credentials.headerName &&
			typeof credentials.headerValue === 'string'
		) {
			requestOptions.headers[credentials.headerName] = credentials.headerValue;
		}

		return requestOptions;
	}
}
