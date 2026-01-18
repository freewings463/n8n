"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/JenkinsApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:JenkinsApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/JenkinsApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/JenkinsApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class JenkinsApi implements ICredentialType {
	name = 'jenkinsApi';

	displayName = 'Jenkins API';

	documentationUrl = 'jenkins';

	properties: INodeProperties[] = [
		{
			displayName: 'Jenkins Username',
			name: 'username',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Personal API Token',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Jenkins Instance URL',
			name: 'baseUrl',
			type: 'string',
			default: '',
		},
	];
}
