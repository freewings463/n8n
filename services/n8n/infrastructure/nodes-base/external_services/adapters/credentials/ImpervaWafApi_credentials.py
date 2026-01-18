"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ImpervaWafApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ImpervaWafApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ImpervaWafApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ImpervaWafApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties } from 'n8n-workflow';

export class ImpervaWafApi implements ICredentialType {
	name = 'impervaWafApi';

	displayName = 'Imperva WAF API';

	documentationUrl = 'impervawaf';

	icon = { light: 'file:icons/Imperva.svg', dark: 'file:icons/Imperva.dark.svg' } as const;

	httpRequestNode = {
		name: 'Imperva WAF',
		docsUrl: 'https://docs.imperva.com/bundle/api-docs',
		apiBaseUrl: 'https://api.imperva.com/',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'API ID',
			name: 'apiID',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'x-API-Id': '={{$credentials.apiID}}',
				'x-API-Key': '={{$credentials.apiKey}}',
			},
		},
	};
}
