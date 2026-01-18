"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/QRadarApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:QRadarApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/QRadarApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/QRadarApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties } from 'n8n-workflow';

export class QRadarApi implements ICredentialType {
	name = 'qRadarApi';

	displayName = 'QRadar API';

	icon = { light: 'file:icons/IBM.svg', dark: 'file:icons/IBM.dark.svg' } as const;

	documentationUrl = 'qradar';

	httpRequestNode = {
		name: 'QRadar',
		docsUrl: 'https://www.ibm.com/docs/en/qradar-common',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				SEC: '={{$credentials.apiKey}}',
			},
		},
	};
}
