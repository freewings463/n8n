"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MicrosoftEntraOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftEntraOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MicrosoftEntraOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MicrosoftEntraOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

const defaultScopes = [
	'openid',
	'offline_access',
	'AccessReview.ReadWrite.All',
	'Directory.ReadWrite.All',
	'NetworkAccessPolicy.ReadWrite.All',
	'DelegatedAdminRelationship.ReadWrite.All',
	'EntitlementManagement.ReadWrite.All',
	'User.ReadWrite.All',
	'Directory.AccessAsUser.All',
	'Sites.FullControl.All',
	'GroupMember.ReadWrite.All',
];

export class MicrosoftEntraOAuth2Api implements ICredentialType {
	name = 'microsoftEntraOAuth2Api';

	displayName = 'Microsoft Entra ID (Azure Active Directory) API';

	extends = ['microsoftOAuth2Api'];

	documentationUrl = 'microsoftentra';

	properties: INodeProperties[] = [
		{
			displayName: 'Custom Scopes',
			name: 'customScopes',
			type: 'boolean',
			default: false,
			description: 'Define custom scopes',
		},
		{
			displayName:
				'The default scopes needed for the node to work are already set, If you change these the node may not function correctly.',
			name: 'customScopesNotice',
			type: 'notice',
			default: '',
			displayOptions: {
				show: {
					customScopes: [true],
				},
			},
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
			description: 'Scopes that should be enabled',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			// Sites.FullControl.All required to update user specific properties https://github.com/microsoftgraph/msgraph-sdk-dotnet/issues/1316
			default:
				'={{$self["customScopes"] ? $self["enabledScopes"] : "' + defaultScopes.join(' ') + '"}}',
		},
	];
}
