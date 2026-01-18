"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PostHog/AliasDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PostHog 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:aliasOperations、aliasFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PostHog/AliasDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PostHog/AliasDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const aliasOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['alias'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an alias',
				action: 'Create an alias',
			},
		],
		default: 'create',
	},
];

export const aliasFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 alias:create                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Alias',
		name: 'alias',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['alias'],
				operation: ['create'],
			},
		},
		default: '',
		description: 'The name of the alias',
	},
	{
		displayName: 'Distinct ID',
		name: 'distinctId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['alias'],
				operation: ['create'],
			},
		},
		default: '',
		description: "The user's distinct ID",
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['alias'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Context',
				name: 'contextUi',
				type: 'fixedCollection',
				placeholder: 'Add Property',
				default: {},
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						displayName: 'Context',
						name: 'contextValues',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								default: '',
							},
						],
					},
				],
			},
			{
				displayName: 'Timestamp',
				name: 'timestamp',
				type: 'dateTime',
				default: '',
				description: "If not set, it'll automatically be set to the current time",
			},
		],
	},
];
