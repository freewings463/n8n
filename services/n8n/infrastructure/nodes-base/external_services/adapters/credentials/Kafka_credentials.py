"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/Kafka.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Kafka。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/Kafka.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/Kafka_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class Kafka implements ICredentialType {
	name = 'kafka';

	displayName = 'Kafka';

	documentationUrl = 'kafka';

	properties: INodeProperties[] = [
		{
			displayName: 'Client ID',
			name: 'clientId',
			type: 'string',
			default: '',
			placeholder: 'my-app',
			hint: 'Will not affect the connection, but will be used to identify the client in the Kafka server logs. Read more <a href="https://kafka.apache.org/documentation/#design_quotasgroups">here</a>',
		},
		{
			displayName: 'Brokers',
			name: 'brokers',
			type: 'string',
			default: '',
			placeholder: 'kafka1:9092,kafka2:9092',
		},
		{
			displayName: 'SSL',
			name: 'ssl',
			type: 'boolean',
			default: true,
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'boolean',
			default: false,
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
			displayOptions: {
				show: {
					authentication: [true],
				},
			},
			default: '',
			description: 'Optional username if authenticated is required',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			displayOptions: {
				show: {
					authentication: [true],
				},
			},
			typeOptions: {
				password: true,
			},
			default: '',
			description: 'Optional password if authenticated is required',
		},
		{
			displayName: 'SASL Mechanism',
			name: 'saslMechanism',
			type: 'options',
			displayOptions: {
				show: {
					authentication: [true],
				},
			},
			options: [
				{
					name: 'Plain',
					value: 'plain',
				},
				{
					name: 'scram-sha-256',
					value: 'scram-sha-256',
				},
				{
					name: 'scram-sha-512',
					value: 'scram-sha-512',
				},
			],
			default: 'plain',
		},
	];
}
