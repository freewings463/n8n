"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/HubspotDeveloperApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:HubspotDeveloperApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/HubspotDeveloperApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/HubspotDeveloperApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

const scopes = [
	'crm.objects.contacts.read',
	'crm.schemas.contacts.read',
	'crm.objects.companies.read',
	'crm.schemas.companies.read',
	'crm.objects.deals.read',
	'crm.schemas.deals.read',
];

// eslint-disable-next-line n8n-nodes-base/cred-class-name-missing-oauth2-suffix
export class HubspotDeveloperApi implements ICredentialType {
	// eslint-disable-next-line n8n-nodes-base/cred-class-field-name-missing-oauth2
	name = 'hubspotDeveloperApi';

	// eslint-disable-next-line n8n-nodes-base/cred-class-field-display-name-missing-oauth2
	displayName = 'HubSpot Developer API';

	documentationUrl = 'hubspot';

	extends = ['oAuth2Api'];

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
			default: 'https://app.hubspot.com/oauth/authorize',
			required: true,
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://api.hubapi.com/oauth/v1/token',
			required: true,
		},
		{
			displayName: 'Auth URI Query Parameters',
			name: 'authQueryParameters',
			type: 'hidden',
			default: 'grant_type=authorization_code',
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'hidden',
			default: 'body',
		},
		{
			displayName: 'Developer API Key',
			name: 'apiKey',
			type: 'string',
			required: true,
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'APP ID',
			name: 'appId',
			type: 'string',
			required: true,
			default: '',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: scopes.join(' '),
		},
	];
}
