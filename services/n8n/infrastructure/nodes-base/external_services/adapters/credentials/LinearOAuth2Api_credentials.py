"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/LinearOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:LinearOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/LinearOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/LinearOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class LinearOAuth2Api implements ICredentialType {
	name = 'linearOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'Linear OAuth2 API';

	documentationUrl = 'linear';

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'hidden',
			default: 'authorizationCode',
		},
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'hidden',
			default: 'https://linear.app/oauth/authorize',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://api.linear.app/oauth/token',
			required: true,
		},
		{
			displayName: 'Actor',
			name: 'actor',
			type: 'options',
			options: [
				{
					name: 'User',
					value: 'user',
					description: 'Resources are created as the user who authorized the application',
				},
				{
					name: 'Application',
					value: 'application',
					description: 'Resources are created as the application',
				},
			],
			default: 'user',
		},
		{
			displayName: 'Include Admin Scope',
			name: 'includeAdminScope',
			type: 'boolean',
			default: false,
			description: 'Grants the "Admin" scope, Needed to create webhooks',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default:
				'={{$self["includeAdminScope"] ? "read write issues:create comments:create admin" : "read write issues:create comments:create"}}',
			required: true,
		},
		{
			displayName: 'Auth URI Query Parameters',
			name: 'authQueryParameters',
			type: 'hidden',
			default: '={{"actor="+$self["actor"]}}',
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'hidden',
			default: 'body',
		},
	];
}
