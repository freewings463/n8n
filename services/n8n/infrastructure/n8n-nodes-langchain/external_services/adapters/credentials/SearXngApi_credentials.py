"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/SearXngApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SearXngApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/SearXngApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/SearXngApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class SearXngApi implements ICredentialType {
	name = 'searXngApi';

	displayName = 'SearXNG';

	documentationUrl = 'searxng';

	properties: INodeProperties[] = [
		{
			displayName: 'API URL',
			name: 'apiUrl',
			type: 'string',
			default: '',
			required: true,
		},
	];
}
