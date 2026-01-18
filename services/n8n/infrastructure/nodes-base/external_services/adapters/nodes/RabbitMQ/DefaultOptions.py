"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/RabbitMQ/DefaultOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/RabbitMQ 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:rabbitDefaultOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/RabbitMQ/DefaultOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/RabbitMQ/DefaultOptions.py

import type { INodeProperties, INodePropertyCollection, INodePropertyOptions } from 'n8n-workflow';

export const rabbitDefaultOptions: Array<
	INodePropertyOptions | INodeProperties | INodePropertyCollection
> = [
	{
		displayName: 'Arguments',
		name: 'arguments',
		placeholder: 'Add Argument',
		description: 'Arguments to add',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		options: [
			{
				name: 'argument',
				displayName: 'Argument',
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
		displayName: 'Headers',
		name: 'headers',
		placeholder: 'Add Header',
		description: 'Headers to add',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		options: [
			{
				name: 'header',
				displayName: 'Header',
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
		displayName: 'Auto Delete Queue',
		name: 'autoDelete',
		type: 'boolean',
		default: false,
		description: 'Whether the queue will be deleted when the number of consumers drops to zero',
	},
	{
		displayName: 'Assert Exchange',
		name: 'assertExchange',
		type: 'boolean',
		default: true,
		description: 'Whether to assert the exchange exists before sending',
	},
	{
		displayName: 'Assert Queue',
		name: 'assertQueue',
		type: 'boolean',
		default: true,
		description: 'Whether to assert the queue exists before sending',
	},
	{
		displayName: 'Durable',
		name: 'durable',
		type: 'boolean',
		default: true,
		description: 'Whether the queue will survive broker restarts',
	},
	{
		displayName: 'Exclusive',
		name: 'exclusive',
		type: 'boolean',
		default: false,
		description: 'Whether to scope the queue to the connection',
	},
];
