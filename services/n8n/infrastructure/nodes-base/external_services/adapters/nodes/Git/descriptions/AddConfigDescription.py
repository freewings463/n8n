"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Git/descriptions/AddConfigDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Git/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ALLOWED_CONFIG_KEYS、addConfigFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Git/descriptions/AddConfigDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Git/descriptions/AddConfigDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const ALLOWED_CONFIG_KEYS = ['user.email', 'user.name', 'remote.origin.url'];

export const addConfigFields: INodeProperties[] = [
	{
		displayName: 'Key',
		name: 'key',
		type: 'options',
		displayOptions: {
			show: {
				operation: ['addConfig'],
				'@version': [{ _cnd: { gte: 1.1 } }],
			},
		},
		options: ALLOWED_CONFIG_KEYS.map((key) => ({
			name: key,
			value: key,
		})),
		default: '',
		description: 'Name of the key to set',
		required: true,
	},
	{
		displayName: 'Key',
		name: 'key',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['addConfig'],
				'@version': [{ _cnd: { lt: 1.1 } }],
			},
		},
		default: '',
		placeholder: 'user.email',
		description: 'Name of the key to set',
		required: true,
	},
	{
		displayName: 'Value',
		name: 'value',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['addConfig'],
			},
		},
		default: '',
		placeholder: 'name@example.com',
		description: 'Value of the key to set',
		required: true,
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		displayOptions: {
			show: {
				operation: ['addConfig'],
			},
		},
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Mode',
				name: 'mode',
				type: 'options',
				options: [
					{
						name: 'Append',
						value: 'append',
					},
					{
						name: 'Set',
						value: 'set',
					},
				],
				default: 'set',
				description: 'Append setting rather than set it in the local config',
			},
		],
	},
];
