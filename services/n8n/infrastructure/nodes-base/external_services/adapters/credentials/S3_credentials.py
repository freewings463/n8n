"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/S3.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:S3。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/S3.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/S3_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class S3 implements ICredentialType {
	name = 's3';

	displayName = 'S3';

	documentationUrl = 's3';

	properties: INodeProperties[] = [
		{
			displayName: 'S3 Endpoint',
			name: 'endpoint',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Region',
			name: 'region',
			type: 'string',
			default: 'us-east-1',
		},
		{
			displayName: 'Access Key ID',
			name: 'accessKeyId',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Secret Access Key',
			name: 'secretAccessKey',
			type: 'string',
			default: '',
			typeOptions: {
				password: true,
			},
		},
		{
			displayName: 'Force Path Style',
			name: 'forcePathStyle',
			type: 'boolean',
			default: false,
		},
		{
			displayName: 'Ignore SSL Issues (Insecure)',
			name: 'ignoreSSLIssues',
			type: 'boolean',
			default: false,
			description: 'Whether to connect even if SSL certificate validation is not possible',
		},
	];
}
