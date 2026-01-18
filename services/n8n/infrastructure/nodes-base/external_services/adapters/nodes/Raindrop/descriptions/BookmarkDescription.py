"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Raindrop/descriptions/BookmarkDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Raindrop/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:bookmarkOperations、bookmarkFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Raindrop/descriptions/BookmarkDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Raindrop/descriptions/BookmarkDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const bookmarkOperations: INodeProperties[] = [
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
				action: 'Create a bookmark',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a bookmark',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a bookmark',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many bookmarks',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a bookmark',
			},
		],
		displayOptions: {
			show: {
				resource: ['bookmark'],
			},
		},
	},
];

export const bookmarkFields: INodeProperties[] = [
	// ----------------------------------
	//       bookmark: create
	// ----------------------------------
	{
		displayName: 'Collection Name or ID',
		name: 'collectionId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		displayOptions: {
			show: {
				resource: ['bookmark'],
				operation: ['create'],
			},
		},
		typeOptions: {
			loadOptionsMethod: 'getCollections',
		},
		default: '',
	},
	{
		displayName: 'Link',
		name: 'link',
		type: 'string',
		required: true,
		default: '',
		description: 'Link of the bookmark to be created',
		displayOptions: {
			show: {
				resource: ['bookmark'],
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
				resource: ['bookmark'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Important',
				name: 'important',
				type: 'boolean',
				default: false,
				description: 'Whether this bookmark is marked as favorite',
			},
			{
				displayName: 'Order',
				name: 'order',
				type: 'number',
				default: 0,
				description:
					'Sort order for the bookmark. For example, to move it to first place, enter 0.',
			},
			{
				displayName: 'Parse Metadata',
				name: 'pleaseParse',
				type: 'boolean',
				default: false,
				description: 'Whether Raindrop should load cover, description and HTML for the URL',
			},
			{
				displayName: 'Tags',
				name: 'tags',
				type: 'string',
				default: '',
				description: 'Bookmark tags. Multiple tags can be set separated by comma.',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Title of the bookmark to create',
			},
		],
	},

	// ----------------------------------
	//       bookmark: delete
	// ----------------------------------
	{
		displayName: 'Bookmark ID',
		name: 'bookmarkId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the bookmark to delete',
		displayOptions: {
			show: {
				resource: ['bookmark'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------
	//       bookmark: get
	// ----------------------------------
	{
		displayName: 'Bookmark ID',
		name: 'bookmarkId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the bookmark to retrieve',
		displayOptions: {
			show: {
				resource: ['bookmark'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//       bookmark: getAll
	// ----------------------------------
	{
		displayName: 'Collection Name or ID',
		name: 'collectionId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getCollections',
		},
		default: [],
		required: true,
		description:
			'The ID of the collection from which to retrieve all bookmarks. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['bookmark'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['bookmark'],
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
				resource: ['bookmark'],
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
	//       bookmark: update
	// ----------------------------------
	{
		displayName: 'Bookmark ID',
		name: 'bookmarkId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the bookmark to update',
		displayOptions: {
			show: {
				resource: ['bookmark'],
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
				resource: ['bookmark'],
				operation: ['update'],
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
			{
				displayName: 'Important',
				name: 'important',
				type: 'boolean',
				default: false,
				description: 'Whether this bookmark is marked as favorite',
			},
			{
				displayName: 'Order',
				name: 'order',
				type: 'number',
				default: 0,
				description:
					'For example if you want to move bookmark to the first place set this field to 0',
			},
			{
				displayName: 'Parse Metadata',
				name: 'pleaseParse',
				type: 'boolean',
				default: false,
				description: 'Whether Raindrop should reload cover, description and HTML for the URL',
			},
			{
				displayName: 'Tags',
				name: 'tags',
				type: 'string',
				default: '',
				description: 'Bookmark tags. Multiple tags can be set separated by comma.',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Title of the bookmark to be created',
			},
		],
	},
];
