"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/HighLevelOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:HighLevelOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/HighLevelOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/HighLevelOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

export class HighLevelOAuth2Api implements ICredentialType {
	name = 'highLevelOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'HighLevel OAuth2 API';

	documentationUrl = 'highlevel';

	icon: Icon = 'file:icons/highLevel.svg';

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
			type: 'options',
			default: 'https://marketplace.leadconnectorhq.com/oauth/chooselocation',
			required: true,
			options: [
				{
					name: 'White-Label',
					value: 'https://marketplace.leadconnectorhq.com/oauth/chooselocation',
				},
				{
					name: 'Standard',
					value: 'https://marketplace.gohighlevel.com/oauth/chooselocation',
				},
			],
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'string',
			hint: "Separate scopes by space, scopes needed for node: 'locations.readonly contacts.readonly contacts.write opportunities.readonly opportunities.write users.readonly'",
			default: '',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://services.leadconnectorhq.com/oauth/token',
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
		{
			displayName:
				'Make sure your credentials include the required OAuth scopes for all actions this node performs.',
			name: 'notice',
			type: 'notice',
			default: '',
			displayOptions: {
				hideOnCloud: true,
			},
		},
	];
}
