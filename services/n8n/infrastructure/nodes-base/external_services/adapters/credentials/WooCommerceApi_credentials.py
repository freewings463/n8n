"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/WooCommerceApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:WooCommerceApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/WooCommerceApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/WooCommerceApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class WooCommerceApi implements ICredentialType {
	name = 'wooCommerceApi';

	displayName = 'WooCommerce API';

	documentationUrl = 'woocommerce';

	properties: INodeProperties[] = [
		{
			displayName: 'Consumer Key',
			name: 'consumerKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Consumer Secret',
			name: 'consumerSecret',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'WooCommerce URL',
			name: 'url',
			type: 'string',
			default: '',
			placeholder: 'https://example.com',
		},
		{
			displayName: 'Include Credentials in Query',
			name: 'includeCredentialsInQuery',
			type: 'boolean',
			default: false,
			description:
				'Whether credentials should be included in the query. Occasionally, some servers may not parse the Authorization header correctly (if you see a “Consumer key is missing” error when authenticating over SSL, you have a server issue). In this case, you may provide the consumer key/secret as query string parameters instead.',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		requestOptions.auth = {
			// @ts-ignore
			user: credentials.consumerKey as string,
			password: credentials.consumerSecret as string,
		};
		if (credentials.includeCredentialsInQuery === true && requestOptions.qs) {
			delete requestOptions.auth;
			Object.assign(requestOptions.qs, {
				consumer_key: credentials.consumerKey,
				consumer_secret: credentials.consumerSecret,
			});
		}
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}/wp-json/wc/v3',
			url: '/products/categories',
		},
	};
}
