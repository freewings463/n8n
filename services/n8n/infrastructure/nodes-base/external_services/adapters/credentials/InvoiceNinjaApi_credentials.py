"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/InvoiceNinjaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:InvoiceNinjaApi。关键函数/方法:authenticate、tokenLength。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/InvoiceNinjaApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/InvoiceNinjaApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class InvoiceNinjaApi implements ICredentialType {
	name = 'invoiceNinjaApi';

	displayName = 'Invoice Ninja API';

	documentationUrl = 'invoiceninja';

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			default: '',
			hint: 'Default URL for v4 is https://app.invoiceninja.com, for v5 it is https://invoicing.co',
		},
		{
			displayName: 'API Token',
			name: 'apiToken',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Secret',
			name: 'secret',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			hint: 'This is optional, enter only if you did set a secret in your app and only if you are using v5',
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials?.url}}',
			url: '/api/v1/clients',
			method: 'GET',
		},
	};

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		const VERSION_5_TOKEN_LENGTH = 64;
		const { apiToken, secret } = credentials;
		const tokenLength = (apiToken as string).length;

		if (tokenLength < VERSION_5_TOKEN_LENGTH) {
			requestOptions.headers = {
				Accept: 'application/json',
				'X-Ninja-Token': apiToken,
			};
		} else {
			requestOptions.headers = {
				'Content-Type': 'application/json',
				'X-API-TOKEN': apiToken,
				'X-Requested-With': 'XMLHttpRequest',
				'X-API-SECRET': secret || '',
			};
		}
		return requestOptions;
	}
}
