"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MarketstackApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MarketstackApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MarketstackApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MarketstackApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class MarketstackApi implements ICredentialType {
	name = 'marketstackApi';

	displayName = 'Marketstack API';

	documentationUrl = 'marketstack';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Use HTTPS',
			name: 'useHttps',
			type: 'boolean',
			default: false,
			description: 'Whether to use HTTPS (paid plans only)',
		},
	];
}
