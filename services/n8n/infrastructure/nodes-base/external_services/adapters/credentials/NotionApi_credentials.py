"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/NotionApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:NotionApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/NotionApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/NotionApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class NotionApi implements ICredentialType {
	name = 'notionApi';

	displayName = 'Notion API';

	documentationUrl = 'notion';

	properties: INodeProperties[] = [
		{
			displayName: 'Internal Integration Secret',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.notion.com/v1',
			url: '/users/me',
		},
	};

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		requestOptions.headers = {
			...requestOptions.headers,
			Authorization: `Bearer ${credentials.apiKey} `,
		};

		// if version it's not set, set it to last one
		// version is only set when the request is made from
		// the notion node, or was set explicitly in the http node
		if (!requestOptions.headers['Notion-Version']) {
			requestOptions.headers = {
				...requestOptions.headers,
				'Notion-Version': '2022-02-22',
			};
		}

		return requestOptions;
	}
}
