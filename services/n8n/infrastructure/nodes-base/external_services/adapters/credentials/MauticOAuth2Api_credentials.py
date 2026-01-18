"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MauticOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MauticOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MauticOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MauticOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class MauticOAuth2Api implements ICredentialType {
	name = 'mauticOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'Mautic OAuth2 API';

	documentationUrl = 'mautic';

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'hidden',
			default: 'authorizationCode',
		},
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			default: '',
			placeholder: 'https://name.mautic.net',
		},
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'hidden',
			default:
				'={{$self["url"].endsWith("/") ? $self["url"].slice(0, -1) : $self["url"]}}/oauth/v2/authorize',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default:
				'={{$self["url"].endsWith("/") ? $self["url"].slice(0, -1) : $self["url"]}}/oauth/v2/token',
			required: true,
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: '',
		},
		{
			displayName: 'Auth URI Query Parameters',
			name: 'authQueryParameters',
			type: 'hidden',
			default: '',
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'hidden',
			default: 'body',
		},
	];
}
