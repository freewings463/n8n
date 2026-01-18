"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ShopifyAccessTokenApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ShopifyAccessTokenApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ShopifyAccessTokenApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ShopifyAccessTokenApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';
export class ShopifyAccessTokenApi implements ICredentialType {
	name = 'shopifyAccessTokenApi';

	displayName = 'Shopify Access Token API';

	documentationUrl = 'shopify';

	properties: INodeProperties[] = [
		{
			displayName: 'Shop Subdomain',
			name: 'shopSubdomain',
			required: true,
			type: 'string',
			default: '',
			description: 'Only the subdomain without .myshopify.com',
		},
		{
			displayName: 'Access Token',
			name: 'accessToken',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'APP Secret Key',
			name: 'appSecretKey',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description: 'Secret key needed to verify the webhook when using Shopify Trigger node',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'X-Shopify-Access-Token': '={{$credentials?.accessToken}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '=https://{{$credentials?.shopSubdomain}}.myshopify.com/admin/api/2024-07',
			url: '/products.json',
		},
	};
}
