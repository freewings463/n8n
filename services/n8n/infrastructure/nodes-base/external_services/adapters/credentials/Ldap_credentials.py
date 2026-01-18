"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/Ldap.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的LDAP凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Ldap。关键函数/方法:无。用于声明 n8n LDAP鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/Ldap.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/Ldap_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

// eslint-disable-next-line n8n-nodes-base/cred-class-name-unsuffixed
export class Ldap implements ICredentialType {
	// eslint-disable-next-line n8n-nodes-base/cred-class-field-name-unsuffixed
	name = 'ldap';

	displayName = 'LDAP';

	documentationUrl = 'ldap';

	properties: INodeProperties[] = [
		{
			displayName: 'LDAP Server Address',
			name: 'hostname',
			type: 'string',
			default: '',
			required: true,
			description: 'IP or domain of the LDAP server',
		},
		{
			displayName: 'LDAP Server Port',
			name: 'port',
			type: 'string',
			default: '389',
			description: 'Port used to connect to the LDAP server',
		},
		{
			displayName: 'Binding DN',
			name: 'bindDN',
			type: 'string',
			default: '',
			description: 'Distinguished Name of the user to connect as',
		},
		{
			displayName: 'Binding Password',
			name: 'bindPassword',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			description: 'Password of the user provided in the Binding DN field above',
		},
		{
			displayName: 'Connection Security',
			name: 'connectionSecurity',
			type: 'options',
			default: 'none',
			options: [
				{
					name: 'None',
					value: 'none',
				},
				{
					name: 'TLS',
					value: 'tls',
				},
				{
					name: 'STARTTLS',
					value: 'startTls',
				},
			],
		},
		{
			displayName: 'Ignore SSL/TLS Issues',
			name: 'allowUnauthorizedCerts',
			type: 'boolean',
			description: 'Whether to connect even if SSL/TLS certificate validation is not possible',
			default: false,
			displayOptions: {
				hide: {
					connectionSecurity: ['none'],
				},
			},
		},
		{
			displayName: 'CA Certificate',
			name: 'caCertificate',
			typeOptions: {
				alwaysOpenEditWindow: true,
			},
			displayOptions: {
				hide: {
					connectionSecurity: ['none'],
				},
			},
			type: 'string',
			default: '',
		},
		{
			displayName: 'Timeout',
			description: 'Optional connection timeout in seconds',
			name: 'timeout',
			type: 'number',
			default: 300,
		},
	];
}
