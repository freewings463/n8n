"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/AirtableOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:AirtableOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/AirtableOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/AirtableOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

const scopes = ['schema.bases:read', 'data.records:read', 'data.records:write'];

export class AirtableOAuth2Api implements ICredentialType {
	name = 'airtableOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'Airtable OAuth2 API';

	documentationUrl = 'airtable';

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'hidden',
			default: 'pkce',
		},
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'hidden',
			default: 'https://airtable.com/oauth2/v1/authorize',
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://airtable.com/oauth2/v1/token',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: `${scopes.join(' ')}`,
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
