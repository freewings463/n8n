"""
MIGRATION-META:
  source_path: packages/nodes-base/utils/sshTunnel.properties.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/utils 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:sshTunnelProperties。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/utils/sshTunnel.properties.ts -> services/n8n/infrastructure/nodes-base/external_services/utils/sshTunnel_properties.py

import type { INodeProperties } from 'n8n-workflow';

export const sshTunnelProperties: INodeProperties[] = [
	{
		displayName: 'SSH Tunnel',
		name: 'sshTunnel',
		type: 'boolean',
		default: false,
	},
	{
		displayName: 'SSH Authenticate with',
		name: 'sshAuthenticateWith',
		type: 'options',
		default: 'password',
		options: [
			{
				name: 'Password',
				value: 'password',
			},
			{
				name: 'Private Key',
				value: 'privateKey',
			},
		],
		displayOptions: {
			show: {
				sshTunnel: [true],
			},
		},
	},
	{
		displayName: 'SSH Host',
		name: 'sshHost',
		type: 'string',
		default: 'localhost',
		displayOptions: {
			show: {
				sshTunnel: [true],
			},
		},
	},
	{
		displayName: 'SSH Port',
		name: 'sshPort',
		type: 'number',
		default: 22,
		displayOptions: {
			show: {
				sshTunnel: [true],
			},
		},
	},
	{
		displayName: 'SSH User',
		name: 'sshUser',
		type: 'string',
		default: 'root',
		displayOptions: {
			show: {
				sshTunnel: [true],
			},
		},
	},
	{
		displayName: 'SSH Password',
		name: 'sshPassword',
		type: 'string',
		typeOptions: {
			password: true,
		},
		default: '',
		displayOptions: {
			show: {
				sshTunnel: [true],
				sshAuthenticateWith: ['password'],
			},
		},
	},
	{
		displayName: 'Private Key',
		name: 'privateKey', // TODO: Rename to sshPrivateKey
		type: 'string',
		typeOptions: {
			rows: 4,
			password: true,
		},
		default: '',
		displayOptions: {
			show: {
				sshTunnel: [true],
				sshAuthenticateWith: ['privateKey'],
			},
		},
	},
	{
		displayName: 'Passphrase',
		name: 'passphrase', // TODO: Rename to sshPassphrase
		type: 'string',
		default: '',
		description: 'Passphrase used to create the key, if no passphrase was used leave empty',
		displayOptions: {
			show: {
				sshTunnel: [true],
				sshAuthenticateWith: ['privateKey'],
			},
		},
	},
];
