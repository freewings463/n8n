"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MicrosoftTeamsOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftTeamsOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MicrosoftTeamsOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MicrosoftTeamsOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class MicrosoftTeamsOAuth2Api implements ICredentialType {
	name = 'microsoftTeamsOAuth2Api';

	extends = ['microsoftOAuth2Api'];

	displayName = 'Microsoft Teams OAuth2 API';

	documentationUrl = 'microsoft';

	properties: INodeProperties[] = [
		//https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default:
				'openid offline_access User.ReadWrite.All Group.ReadWrite.All Chat.ReadWrite ChannelMessage.Read.All',
		},
		{
			displayName: `
      Microsoft Teams Trigger requires the following permissions:
      <br><code>ChannelMessage.Read.All</code>
      <br><code>Chat.Read.All</code>
      <br><code>Team.ReadBasic.All</code>
      <br><code>Subscription.ReadWrite.All</code>
      <br>Configure these permissions in <a href="https://portal.azure.com">Microsoft Entra</a>
    `,
			name: 'notice',
			type: 'notice',
			default: '',
		},
	];
}
