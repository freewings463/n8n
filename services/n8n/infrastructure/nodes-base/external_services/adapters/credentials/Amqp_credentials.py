"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/Amqp.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Amqp。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/Amqp.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/Amqp_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class Amqp implements ICredentialType {
	name = 'amqp';

	displayName = 'AMQP';

	documentationUrl = 'amqp';

	properties: INodeProperties[] = [
		{
			displayName: 'Hostname',
			name: 'hostname',
			type: 'string',
			placeholder: 'e.g. localhost',
			default: '',
		},
		{
			displayName: 'Port',
			name: 'port',
			type: 'number',
			default: 5672,
		},
		{
			displayName: 'User',
			name: 'username',
			type: 'string',
			placeholder: 'e.g. guest',
			default: '',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			placeholder: 'e.g. guest',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Transport Type',
			name: 'transportType',
			type: 'string',
			placeholder: 'e.g. tcp',
			default: '',
			hint: 'Optional transport type to use, either tcp or tls',
		},
	];
}
