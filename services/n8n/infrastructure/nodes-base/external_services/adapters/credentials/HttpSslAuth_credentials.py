"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/HttpSslAuth.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:HttpSslAuth。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。注释目标:eslint-disable n8n-nodes-base/cred-class-name-unsuffixed。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/HttpSslAuth.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/HttpSslAuth_credentials.py

/* eslint-disable n8n-nodes-base/cred-class-name-unsuffixed */
/* eslint-disable n8n-nodes-base/cred-class-field-name-unsuffixed */
import type { ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

export class HttpSslAuth implements ICredentialType {
	name = 'httpSslAuth';

	displayName = 'SSL Certificates';

	documentationUrl = 'httprequest';

	icon: Icon = 'node:n8n-nodes-base.httpRequest';

	properties: INodeProperties[] = [
		{
			displayName: 'CA',
			name: 'ca',
			type: 'string',
			description: 'Certificate Authority certificate',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Certificate',
			name: 'cert',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Private Key',
			name: 'key',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Passphrase',
			name: 'passphrase',
			type: 'string',
			description: 'Optional passphrase for the private key, if the private key is encrypted',
			typeOptions: {
				password: true,
			},
			default: '',
		},
	];
}
