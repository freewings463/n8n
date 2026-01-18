"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/OrbitApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:OrbitApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/OrbitApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/OrbitApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class OrbitApi implements ICredentialType {
	name = 'orbitApi';

	displayName = 'Orbit API';

	documentationUrl = 'orbit';

	properties: INodeProperties[] = [
		{
			displayName:
				'Orbit has been shutdown and will no longer function from July 11th, You can read more <a target="_blank" href="https://orbit.love/blog/orbit-is-joining-postman">here</a>.',
			name: 'deprecated',
			type: 'notice',
			default: '',
		},
		{
			displayName: 'API Token',
			name: 'accessToken',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];
}
