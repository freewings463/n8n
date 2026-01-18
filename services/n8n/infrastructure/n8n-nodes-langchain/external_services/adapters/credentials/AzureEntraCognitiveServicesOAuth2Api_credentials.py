"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/AzureEntraCognitiveServicesOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:AzureEntraCognitiveServicesOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/AzureEntraCognitiveServicesOAuth2Api.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/AzureEntraCognitiveServicesOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

const defaultScopes = ['openid', 'offline_access'];

export class AzureEntraCognitiveServicesOAuth2Api implements ICredentialType {
	name = 'azureEntraCognitiveServicesOAuth2Api';

	// eslint-disable-next-line n8n-nodes-base/cred-class-field-display-name-missing-oauth2
	displayName = 'Azure Entra ID (Azure Active Directory) API';

	extends = ['oAuth2Api'];

	documentationUrl = 'azureentracognitiveservicesoauth2api';

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'hidden',
			default: 'authorizationCode',
		},
		{
			displayName: 'Resource Name',
			name: 'resourceName',
			type: 'string',
			required: true,
			default: '',
		},
		{
			displayName: 'API Version',
			name: 'apiVersion',
			type: 'string',
			required: true,
			default: '2025-03-01-preview',
		},
		{
			displayName: 'Endpoint',
			name: 'endpoint',
			type: 'string',
			default: undefined,
			placeholder: 'https://westeurope.api.cognitive.microsoft.com',
		},
		{
			displayName: 'Tenant ID',
			name: 'tenantId',
			type: 'string',
			default: 'common',
			description:
				'Enter your Azure Tenant ID (Directory ID) or keep "common" for multi-tenant apps. Using a specific Tenant ID is generally recommended and required for certain authentication flows.',
			placeholder: 'e.g., xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx or common',
		},
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'hidden',
			default: '=https://login.microsoftonline.com/{{$self["tenantId"]}}/oauth2/authorize',
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: '=https://login.microsoftonline.com/{{$self["tenantId"]}}/oauth2/token',
		},
		{
			displayName: 'Additional Body Properties',
			name: 'additionalBodyProperties',
			type: 'hidden',
			default:
				'{"grant_type": "client_credentials", "resource": "https://cognitiveservices.azure.com/"}',
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'hidden',
			default: 'body',
		},
		{
			displayName: 'Custom Scopes',
			name: 'customScopes',
			type: 'boolean',
			default: false,
			description:
				'Define custom scopes. You might need this if the default scopes are not sufficient or if you want to minimize permissions. Ensure you include "openid" and "offline_access".',
		},
		{
			displayName: 'Auth URI Query Parameters',
			name: 'authQueryParameters',
			type: 'hidden',
			default: '',
			description:
				'For some services additional query parameters have to be set which can be defined here',
			placeholder: '',
		},
		{
			displayName: 'Enabled Scopes',
			name: 'enabledScopes',
			type: 'string',
			displayOptions: {
				show: {
					customScopes: [true],
				},
			},
			default: defaultScopes.join(' '),
			placeholder: 'openid offline_access',
			description: 'Space-separated list of scopes to request.',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: '={{ $self.customScopes ? $self.enabledScopes : "' + defaultScopes.join(' ') + '"}}',
		},
	];
}
