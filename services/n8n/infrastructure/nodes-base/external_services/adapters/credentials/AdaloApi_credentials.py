"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/AdaloApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:AdaloApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/AdaloApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/AdaloApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties } from 'n8n-workflow';

export class AdaloApi implements ICredentialType {
	name = 'adaloApi';

	displayName = 'Adalo API';

	documentationUrl = 'adalo';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description:
				'The Adalo API is available on paid Adalo plans, find more information <a href="https://help.adalo.com/integrations/the-adalo-api" target="_blank">here</a>',
		},
		{
			displayName: 'App ID',
			name: 'appId',
			type: 'string',
			default: '',
			description:
				'You can get App ID from the URL of your app. For example, if your app URL is <strong>https://app.adalo.com/apps/1234567890/screens</strong>, then your App ID is <strong>1234567890</strong>.',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiKey}}',
			},
		},
	};
}
