"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Raindrop/descriptions/CollectionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Raindrop/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:collectionOperations、collectionFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Raindrop/descriptions/CollectionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Raindrop/descriptions/CollectionDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const collectionOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a collection',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a collection',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a collection',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many collections',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a collection',
			},
		],
		displayOptions: {
			show: {
				resource: ['collection'],
			},
		},
	},
];

export const collectionFields: INodeProperties[] = [
	// ----------------------------------
	//       collection: create
	// ----------------------------------
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		required: true,
		default: '',
		description: 'Title of the collection to create',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Cover',
				name: 'cover',
				type: 'string',
				default: '',
				description: 'URL of an image to use as cover for the collection',
			},
			{
				displayName: 'Public',
				name: 'public',
				type: 'boolean',
				default: false,
				description: 'Whether the collection will be accessible without authentication',
			},
			{
				displayName: 'Parent ID',
				name: 'parentId',
				type: 'string',
				default: '',
				description: "ID of this collection's parent collection, if it is a child collection",
			},
			{
				displayName: 'Sort Order',
				name: 'sort',
				type: 'number',
				default: 1,
				description:
					'Descending sort order of this collection. The number is the position of the collection among all the collections with the same parent ID.',
			},
			{
				displayName: 'View',
				name: 'view',
				type: 'options',
				default: 'list',
				description: 'View style of this collection',
				options: [
					{
						name: 'List',
						value: 'list',
					},
					{
						name: 'Simple',
						value: 'simple',
					},
					{
						name: 'Grid',
						value: 'grid',
					},
					{
						name: 'Masonry',
						value: 'Masonry',
					},
				],
			},
		],
	},

	// ----------------------------------
	//       collection: delete
	// ----------------------------------
	{
		displayName: 'Collection ID',
		name: 'collectionId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the collection to delete',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------
	//       collection: get
	// ----------------------------------
	{
		displayName: 'Collection ID',
		name: 'collectionId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the collection to retrieve',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//       collection: getAll
	// ----------------------------------
	{
		displayName: 'Type',
		name: 'type',
		type: 'options',
		required: true,
		default: 'parent',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				name: 'Parent',
				value: 'parent',
				description: 'Root-level collections',
			},
			{
				name: 'Children',
				value: 'children',
				description: 'Nested collections',
			},
		],
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['collection'],
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
				resource: ['collection'],
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

	// ----------------------------------
	//       collection: update
	// ----------------------------------
	{
		displayName: 'Collection ID',
		name: 'collectionId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the collection to update',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Cover',
				name: 'cover',
				type: 'string',
				default: 'data',
				placeholder: '',
				description:
					'Name of the binary property containing the data for the image to upload as a cover',
			},
			{
				displayName: 'Public',
				name: 'public',
				type: 'boolean',
				default: false,
				description: 'Whether the collection will be accessible without authentication',
			},
			{
				displayName: 'Parent ID',
				name: 'parentId',
				type: 'string',
				default: '',
				description: "ID of this collection's parent collection, if it is a child collection",
			},
			{
				displayName: 'Sort Order',
				name: 'sort',
				type: 'number',
				default: 1,
				description:
					'Descending sort order of this collection. The number is the position of the collection among all the collections with the same parent ID.',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Title of the collection to update',
			},
			{
				displayName: 'View',
				name: 'view',
				type: 'options',
				default: 'list',
				description: 'View style of this collection',
				options: [
					{
						name: 'List',
						value: 'list',
					},
					{
						name: 'Simple',
						value: 'simple',
					},
					{
						name: 'Grid',
						value: 'grid',
					},
					{
						name: 'Masonry',
						value: 'Masonry',
					},
				],
			},
		],
	},
];
