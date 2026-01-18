"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/AzureAiSearchApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:AzureAiSearchApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/AzureAiSearchApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/AzureAiSearchApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class AzureAiSearchApi implements ICredentialType {
	name = 'azureAiSearchApi';

	displayName = 'Azure AI Search API';

	documentationUrl = 'azureaisearch';

	properties: INodeProperties[] = [
		{
			displayName: 'Search Endpoint',
			name: 'endpoint',
			type: 'string',
			required: true,
			default: '',
			placeholder: 'https://your-search-service.search.windows.net',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
		},
	];

	authenticate = async (
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> => {
		return {
			...requestOptions,
			headers: {
				...requestOptions.headers,
				'api-key': credentials.apiKey,
			},
		};
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.endpoint}}/indexes',
			url: '',
			method: 'GET',
			headers: {
				accept: 'application/json',
			},
			qs: {
				'api-version': '2024-07-01',
			},
		},
	};
}
