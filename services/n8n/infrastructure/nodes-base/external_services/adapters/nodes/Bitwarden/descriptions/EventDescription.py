"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Bitwarden/descriptions/EventDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Bitwarden/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventOperations、eventFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Bitwarden/descriptions/EventDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Bitwarden/descriptions/EventDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const eventOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many events',
			},
		],
		displayOptions: {
			show: {
				resource: ['event'],
			},
		},
	},
];

export const eventFields: INodeProperties[] = [
	// ----------------------------------
	//       event: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		typeOptions: {
			minValue: 1,
		},
		default: 10,
		description: 'Max number of results to return',
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		options: [
			{
				displayName: 'Acting User ID',
				name: 'actingUserId',
				type: 'string',
				default: '',
				description: 'The unique identifier of the acting user',
				placeholder: '4a59c8c7-e05a-4d17-8e85-acc301343926',
			},
			{
				displayName: 'End Date',
				name: 'end',
				type: 'dateTime',
				default: '',
				description: 'The end date for the search',
			},
			{
				displayName: 'Item ID',
				name: 'itemID',
				type: 'string',
				default: '',
				description: 'The unique identifier of the item that the event describes',
				placeholder: '5e59c8c7-e05a-4d17-8e85-acc301343926',
			},
			{
				displayName: 'Start Date',
				name: 'start',
				type: 'dateTime',
				default: '',
				description: 'The start date for the search',
			},
		],
		displayOptions: {
			show: {
				resource: ['event'],
				operation: ['getAll'],
			},
		},
	},
];
