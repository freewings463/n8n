"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MySql.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:@utils/sshTunnel.properties；内部:n8n-workflow；本地:无。导出:MySql。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MySql.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MySql_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

import { sshTunnelProperties } from '@utils/sshTunnel.properties';

export class MySql implements ICredentialType {
	name = 'mySql';

	displayName = 'MySQL';

	documentationUrl = 'mysql';

	properties: INodeProperties[] = [
		{
			displayName: 'Host',
			name: 'host',
			type: 'string',
			default: 'localhost',
		},
		{
			displayName: 'Database',
			name: 'database',
			type: 'string',
			default: 'mysql',
		},
		{
			displayName: 'User',
			name: 'user',
			type: 'string',
			default: 'mysql',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Port',
			name: 'port',
			type: 'number',
			default: 3306,
		},
		{
			displayName: 'Connect Timeout',
			name: 'connectTimeout',
			type: 'number',
			default: 10000,
			description:
				'The milliseconds before a timeout occurs during the initial connection to the MySQL server',
		},
		{
			displayName: 'SSL',
			name: 'ssl',
			type: 'boolean',
			default: false,
		},
		{
			displayName: 'CA Certificate',
			name: 'caCertificate',
			typeOptions: {
				password: true,
			},
			displayOptions: {
				show: {
					ssl: [true],
				},
			},
			type: 'string',
			default: '',
		},
		{
			displayName: 'Client Private Key',
			name: 'clientPrivateKey',
			typeOptions: {
				password: true,
			},
			displayOptions: {
				show: {
					ssl: [true],
				},
			},
			type: 'string',
			default: '',
		},
		{
			displayName: 'Client Certificate',
			name: 'clientCertificate',
			typeOptions: {
				password: true,
			},
			displayOptions: {
				show: {
					ssl: [true],
				},
			},
			type: 'string',
			default: '',
		},
		...sshTunnelProperties,
	];
}
