"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/AzureStorageOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:AzureStorageOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/AzureStorageOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/AzureStorageOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class AzureStorageOAuth2Api implements ICredentialType {
	name = 'azureStorageOAuth2Api';

	displayName = 'Azure Storage OAuth2 API';

	extends = ['microsoftOAuth2Api'];

	documentationUrl = 'azurestorage';

	properties: INodeProperties[] = [
		{
			displayName: 'Account',
			name: 'account',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'hidden',
			default: '=https://{{ $self["account"] }}.blob.core.windows.net',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: 'https://storage.azure.com/.default',
		},
	];
}
