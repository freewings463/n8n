"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MalcoreApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:MalcoreApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MalcoreApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MalcoreApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class MalcoreApi implements ICredentialType {
	name = 'malcoreApi';

	displayName = 'MalcoreAPI';

	documentationUrl = 'malcore';

	icon = { light: 'file:icons/Malcore.png', dark: 'file:icons/Malcore.png' } as const;

	httpRequestNode = {
		name: 'Malcore',
		docsUrl: 'https://malcore.readme.io/reference/upload',
		apiBaseUrlPlaceholder: 'https://api.malcore.io/api/urlcheck',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				apiKey: '={{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.malcore.io/api',
			url: '/urlcheck',
			method: 'POST',
			body: { url: 'google.com' },
		},
	};
}
