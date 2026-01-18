"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/GongOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:GongOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/GongOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/GongOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class GongOAuth2Api implements ICredentialType {
	name = 'gongOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'Gong OAuth2 API';

	documentationUrl = 'gong';

	properties: INodeProperties[] = [
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'string',
			default: 'https://api.gong.io',
		},
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
			default: 'https://app.gong.io/oauth2/authorize',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://app.gong.io/oauth2/generate-customer-token',
			required: true,
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default:
				'api:calls:read:transcript api:provisioning:read api:workspaces:read api:meetings:user:delete api:crm:get-objects api:data-privacy:delete api:crm:schema api:flows:write api:crm:upload api:meetings:integration:status api:calls:read:extensive api:meetings:user:update api:integration-settings:write api:settings:scorecards:read api:stats:scorecards api:stats:interaction api:stats:user-actions api:crm:integration:delete api:calls:read:basic api:calls:read:media-url api:digital-interactions:write api:crm:integrations:read api:library:read api:data-privacy:read api:users:read api:logs:read api:calls:create api:meetings:user:create api:stats:user-actions:detailed api:settings:trackers:read api:crm:integration:register api:provisioning:read-write api:engagement-data:write api:permission-profile:read api:permission-profile:write api:flows:read api:crm-calls:manual-association:read',
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
			default: 'header',
		},
	];
}
