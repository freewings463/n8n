"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/OAuth1Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:OAuth1Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/OAuth1Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/OAuth1Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class OAuth1Api implements ICredentialType {
	name = 'oAuth1Api';

	displayName = 'OAuth1 API';

	documentationUrl = 'httprequest';

	genericAuth = true;

	properties: INodeProperties[] = [
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Consumer Key',
			name: 'consumerKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
		},
		{
			displayName: 'Consumer Secret',
			name: 'consumerSecret',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
		},
		{
			displayName: 'Request Token URL',
			name: 'requestTokenUrl',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Signature Method',
			name: 'signatureMethod',
			type: 'options',
			options: [
				{
					name: 'HMAC-SHA1',
					value: 'HMAC-SHA1',
				},
				{
					name: 'HMAC-SHA256',
					value: 'HMAC-SHA256',
				},
				{
					name: 'HMAC-SHA512',
					value: 'HMAC-SHA512',
				},
			],
			default: 'HMAC-SHA1',
			required: true,
		},
	];
}
