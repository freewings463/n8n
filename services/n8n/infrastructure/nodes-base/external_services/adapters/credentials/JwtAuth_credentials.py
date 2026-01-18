"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/JwtAuth.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的JWT凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:JwtAuth。关键函数/方法:无。用于声明 n8n JWT鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/JwtAuth.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/JwtAuth_credentials.py

import type { ICredentialType, INodeProperties, INodePropertyOptions, Icon } from 'n8n-workflow';

const algorithms: INodePropertyOptions[] = [
	{
		name: 'HS256',
		value: 'HS256',
	},
	{
		name: 'HS384',
		value: 'HS384',
	},
	{
		name: 'HS512',
		value: 'HS512',
	},
	{
		name: 'RS256',
		value: 'RS256',
	},
	{
		name: 'RS384',
		value: 'RS384',
	},
	{
		name: 'RS512',
		value: 'RS512',
	},
	{
		name: 'ES256',
		value: 'ES256',
	},
	{
		name: 'ES384',
		value: 'ES384',
	},
	{
		name: 'ES512',
		value: 'ES512',
	},
	{
		name: 'PS256',
		value: 'PS256',
	},
	{
		name: 'PS384',
		value: 'PS384',
	},
	{
		name: 'PS512',
		value: 'PS512',
	},
	{
		name: 'none',
		value: 'none',
	},
];

// eslint-disable-next-line n8n-nodes-base/cred-class-name-unsuffixed
export class JwtAuth implements ICredentialType {
	// eslint-disable-next-line n8n-nodes-base/cred-class-field-name-unsuffixed
	name = 'jwtAuth';

	displayName = 'JWT Auth';

	documentationUrl = 'jwt';

	icon: Icon = 'file:icons/jwt.svg';

	properties: INodeProperties[] = [
		{
			displayName: 'Key Type',
			name: 'keyType',
			type: 'options',
			description: 'Choose either the secret passphrase or PEM encoded public keys',
			options: [
				{
					name: 'Passphrase',
					value: 'passphrase',
				},
				{
					name: 'PEM Key',
					value: 'pemKey',
				},
			],
			default: 'passphrase',
		},
		{
			displayName: 'Secret',
			name: 'secret',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			displayOptions: {
				show: {
					keyType: ['passphrase'],
				},
			},
		},
		{
			displayName: 'Private Key',
			name: 'privateKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			displayOptions: {
				show: {
					keyType: ['pemKey'],
				},
			},
			default: '',
		},
		{
			displayName: 'Public Key',
			name: 'publicKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			displayOptions: {
				show: {
					keyType: ['pemKey'],
				},
			},
			default: '',
		},
		{
			displayName: 'Algorithm',
			name: 'algorithm',
			type: 'options',
			default: 'HS256',
			options: algorithms,
		},
	];
}
