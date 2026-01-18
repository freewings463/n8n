"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HomeAssistant/EventDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HomeAssistant 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventOperations、eventFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HomeAssistant/EventDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HomeAssistant/EventDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const eventOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['event'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an event',
				action: 'Create an event',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many events',
				action: 'Get many events',
			},
		],
		default: 'getAll',
	},
];

export const eventFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                event:getAll                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['event'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['event'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 50,
		description: 'Max number of results to return',
	},

	/* -------------------------------------------------------------------------- */
	/*                                event:create                                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Event Type',
		name: 'eventType',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['event'],
			},
		},
		required: true,
		default: '',
		description: 'The Entity ID for which an event will be created',
	},
	{
		displayName: 'Event Attributes',
		name: 'eventAttributes',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		placeholder: 'Add Attribute',
		default: {},
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Attributes',
				name: 'attributes',
				values: [
					{
						displayName: 'Name',
						name: 'name',
						type: 'string',
						default: '',
						description: 'Name of the attribute',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the attribute',
					},
				],
			},
		],
	},
];
