"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MicrosoftAzureMonitorOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftAzureMonitorOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MicrosoftAzureMonitorOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MicrosoftAzureMonitorOAuth2Api_credentials.py

import type { Icon, ICredentialType, INodeProperties } from 'n8n-workflow';

export class MicrosoftAzureMonitorOAuth2Api implements ICredentialType {
	name = 'microsoftAzureMonitorOAuth2Api';

	displayName = 'Microsoft Azure Monitor OAuth2 API';

	extends = ['oAuth2Api'];

	documentationUrl = 'microsoftazuremonitor';

	icon: Icon = 'file:icons/Microsoft.svg';

	httpRequestNode = {
		name: 'Microsoft Azure Monitor',
		docsUrl: 'https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/request-format',
		apiBaseUrlPlaceholder: 'https://api.loganalytics.azure.com/v1/workspaces/[workspace_id]/query',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'options',
			options: [
				{
					name: 'Authorization Code',
					value: 'authorizationCode',
				},
				{
					name: 'Client Credentials',
					value: 'clientCredentials',
				},
			],
			default: 'authorizationCode',
		},
		{
			displayName: 'Tenant ID',
			required: true,
			name: 'tenantId',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			options: [
				{
					name: 'Azure Log Analytics',
					value: 'https://api.loganalytics.azure.com',
				},
				{
					name: 'Log Analytics',
					value: 'https://api.loganalytics.io',
				},
				{
					name: 'Azure Monitor',
					value: 'https://monitor.azure.com',
				},
				{
					name: 'Azure Management',
					value: 'https://management.azure.com',
				},
			],
			default: 'https://api.loganalytics.azure.com',
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
			default:
				'=https://login.microsoftonline.com/{{$self["tenantId"]}}/oauth2/{{$self["grantType"] === "clientCredentials" ? "v2.0/" : ""}}token',
		},
		{
			displayName: 'Auth URI Query Parameters',
			name: 'authQueryParameters',
			type: 'hidden',
			default:
				'={{$self["grantType"] === "clientCredentials" ? "" : "resource=" + $self["resource"]}}',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default:
				'={{$self["grantType"] === "clientCredentials" ? $self["resource"] + "/.default" : ""}}',
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'hidden',
			default: 'body',
		},
	];
}
