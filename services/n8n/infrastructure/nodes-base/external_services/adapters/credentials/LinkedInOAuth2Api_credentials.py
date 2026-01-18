"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/LinkedInOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:LinkedInOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/LinkedInOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/LinkedInOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class LinkedInOAuth2Api implements ICredentialType {
	name = 'linkedInOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'LinkedIn OAuth2 API';

	documentationUrl = 'linkedin';

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'hidden',
			default: 'authorizationCode',
		},
		{
			displayName: 'Organization Support',
			name: 'organizationSupport',
			type: 'boolean',
			default: true,
			description: 'Whether to request permissions to post as an organization',
		},
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'hidden',
			default: 'https://www.linkedin.com/oauth/v2/authorization',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://www.linkedin.com/oauth/v2/accessToken',
			required: true,
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default:
				'=w_member_social{{$self["organizationSupport"] === true ? ",w_organization_social": $self["legacy"] === true ? ",r_liteprofile,r_emailaddress" : ",profile,email,openid"}}',
			description:
				'Standard scopes for posting on behalf of a user or organization. See <a href="https://docs.microsoft.com/en-us/linkedin/marketing/getting-started#available-permissions"> this resource </a>.',
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
			displayName: 'Legacy',
			name: 'legacy',
			type: 'boolean',
			default: true,
			description: 'Whether to use the legacy API',
		},
	];
}
