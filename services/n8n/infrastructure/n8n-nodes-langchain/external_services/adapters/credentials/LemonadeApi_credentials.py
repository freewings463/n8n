"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/LemonadeApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:LemonadeApiCredentialsType、LemonadeApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/LemonadeApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/LemonadeApi_credentials.py

import type {
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
	IHttpRequestOptions,
	ICredentialDataDecryptedObject,
} from 'n8n-workflow';

export type LemonadeApiCredentialsType = {
	baseUrl: string;
	apiKey?: string;
};

export class LemonadeApi implements ICredentialType {
	name = 'lemonadeApi';

	displayName = 'Lemonade';

	documentationUrl = 'lemonade';

	properties: INodeProperties[] = [
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			required: true,
			type: 'string',
			default: 'http://localhost:8000/api/v1',
		},
		{
			displayName: 'API Key',
			hint: 'Optional API key for Lemonade server authentication. Not required for default Lemonade installation',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: false,
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		// Only add Authorization header if API key is provided and not empty
		const apiKey = credentials.apiKey as string | undefined;
		if (apiKey && apiKey.trim() !== '') {
			requestOptions.headers = {
				...requestOptions.headers,
				Authorization: `Bearer ${apiKey}`,
			};
		}
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{ $credentials.baseUrl }}',
			url: '/models',
			method: 'GET',
		},
	};
}
