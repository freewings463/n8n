"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/YourlsApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:YourlsApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/YourlsApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/YourlsApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class YourlsApi implements ICredentialType {
	name = 'yourlsApi';

	displayName = 'Yourls API';

	documentationUrl = 'yourls';

	properties: INodeProperties[] = [
		{
			displayName: 'Signature',
			name: 'signature',
			type: 'string',
			default: '',
		},
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			default: '',
			placeholder: 'http://localhost:8080',
		},
	];
}
