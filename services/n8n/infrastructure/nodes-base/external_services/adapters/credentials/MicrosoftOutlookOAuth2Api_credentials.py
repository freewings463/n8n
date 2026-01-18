"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MicrosoftOutlookOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftOutlookOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MicrosoftOutlookOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MicrosoftOutlookOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

const scopes = [
	'openid',
	'offline_access',
	'Contacts.Read',
	'Contacts.ReadWrite',
	'Calendars.Read',
	'Calendars.Read.Shared',
	'Calendars.ReadWrite',
	'Mail.ReadWrite',
	'Mail.ReadWrite.Shared',
	'Mail.Send',
	'Mail.Send.Shared',
	'MailboxSettings.Read',
];

export class MicrosoftOutlookOAuth2Api implements ICredentialType {
	name = 'microsoftOutlookOAuth2Api';

	extends = ['microsoftOAuth2Api'];

	displayName = 'Microsoft Outlook OAuth2 API';

	documentationUrl = 'microsoft';

	properties: INodeProperties[] = [
		//https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: scopes.join(' '),
		},
		{
			displayName: 'Use Shared Mailbox',
			name: 'useShared',
			type: 'boolean',
			default: false,
		},
		{
			displayName: 'User Principal Name',
			name: 'userPrincipalName',
			description: "Target user's UPN or ID",
			type: 'string',
			default: '',
			displayOptions: {
				show: {
					useShared: [true],
				},
			},
		},
	];
}
