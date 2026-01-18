"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Raindrop/descriptions/TagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Raindrop/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:tagOperations、tagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Raindrop/descriptions/TagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Raindrop/descriptions/TagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const tagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a tag',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many tags',
			},
		],
		displayOptions: {
			show: {
				resource: ['tag'],
			},
		},
	},
];

export const tagFields: INodeProperties[] = [
	// ----------------------------------
	//       tag: delete
	// ----------------------------------
	{
		displayName: 'Tags',
		name: 'tags',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['delete'],
			},
		},
		description:
			'One or more tags to delete. Enter comma-separated values to delete multiple tags.',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['delete'],
			},
		},
		options: [
			{
				displayName: 'Collection Name or ID',
				name: 'collectionId',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getCollections',
				},
				default: '',
				description:
					'It\'s possible to restrict remove action to just one collection. It\'s optional. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
			},
		],
	},
	// ----------------------------------
	//       tag: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['getAll'],
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
				resource: ['tag'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 10,
		},
		default: 5,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Collection Name or ID',
				name: 'collectionId',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				typeOptions: {
					loadOptionsMethod: 'getCollections',
				},
				default: '',
			},
		],
	},
];
