"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MicrosoftSharePointOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftSharePointOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MicrosoftSharePointOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MicrosoftSharePointOAuth2Api_credentials.py

import type { Icon, ICredentialType, INodeProperties } from 'n8n-workflow';

export class MicrosoftSharePointOAuth2Api implements ICredentialType {
	name = 'microsoftSharePointOAuth2Api';

	extends = ['microsoftOAuth2Api'];

	icon: Icon = {
		light: 'file:icons/microsoftSharePoint.svg',
		dark: 'file:icons/microsoftSharePoint.svg',
	};

	displayName = 'Microsoft SharePoint OAuth2 API';

	documentationUrl = 'microsoft';

	httpRequestNode = {
		name: 'Microsoft SharePoint',
		docsUrl: 'https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-graph',
		apiBaseUrlPlaceholder: 'https://{subdomain}.sharepoint.com/_api/v2.0/',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: '=openid offline_access https://{{$self.subdomain}}.sharepoint.com/.default',
		},
		{
			displayName: 'Subdomain',
			name: 'subdomain',
			type: 'string',
			default: '',
			hint: 'You can extract the subdomain from the URL. For example, in the URL "https://tenant123.sharepoint.com", the subdomain is "tenant123".',
		},
	];
}
