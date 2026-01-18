"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wekan/BoardDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wekan 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:boardOperations、boardFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wekan/BoardDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wekan/BoardDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const boardOperations: INodeProperties[] = [
	// ----------------------------------
	//         board
	// ----------------------------------
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['board'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new board',
				action: 'Create a board',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a board',
				action: 'Delete a board',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get the data of a board',
				action: 'Get a board',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many user boards',
				action: 'Get many boards',
			},
		],
		default: 'create',
	},
];

export const boardFields: INodeProperties[] = [
	// ----------------------------------
	//         board:create
	// ----------------------------------
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		default: '',
		placeholder: 'My board',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['board'],
			},
		},
		description: 'The title of the board',
	},
	{
		displayName: 'Owner Name or ID',
		name: 'owner',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['board'],
			},
		},
		description:
			'The user ID in Wekan. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['board'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Active',
				name: 'isActive',
				type: 'boolean',
				default: false,
				description: 'Whether to set the board active',
			},
			{
				displayName: 'Admin',
				name: 'isAdmin',
				type: 'boolean',
				default: false,
				description: 'Whether to set the owner an admin of the board',
			},
			{
				displayName: 'Color',
				name: 'color',
				type: 'options',
				options: [
					{
						name: 'Belize',
						value: 'belize',
					},
					{
						name: 'Midnight',
						value: 'midnight',
					},
					{
						name: 'Nephritis',
						value: 'nephritis',
					},
					{
						name: 'Pomegranate',
						value: 'pomegranate',
					},
					{
						name: 'Pumpkin',
						value: 'pumpkin',
					},
					{
						name: 'Wisteria',
						value: 'wisteria',
					},
				],
				default: '',
				description: 'The color of the board',
			},
			{
				displayName: 'Comment Only',
				name: 'isCommentOnly',
				type: 'boolean',
				default: false,
				description: 'Whether to enable comments',
			},
			{
				displayName: 'No Comments',
				name: 'isNoComments',
				type: 'boolean',
				default: false,
				description: 'Whether to disable comments',
			},
			{
				displayName: 'Permission',
				name: 'permission',
				type: 'options',
				options: [
					{
						name: 'Private',
						value: 'private',
					},
					{
						name: 'Public',
						value: 'public',
					},
				],
				default: 'private',
				description: 'Set the board permission',
			},
			{
				displayName: 'Worker',
				name: 'isWorker',
				type: 'boolean',
				default: false,
				description: 'Whether to only move cards, assign himself to card and comment',
			},
		],
	},

	// ----------------------------------
	//         board:delete
	// ----------------------------------
	{
		displayName: 'Board ID',
		name: 'boardId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['board'],
			},
		},
		description: 'The ID of the board to delete',
	},

	// ----------------------------------
	//         board:get
	// ----------------------------------
	{
		displayName: 'Board ID',
		name: 'boardId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['board'],
			},
		},
		description: 'The ID of the board to get',
	},

	// ----------------------------------
	//         board:getAll
	// ----------------------------------
	{
		displayName: 'User Name or ID',
		name: 'IdUser',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['board'],
			},
		},
		description:
			'The ID of the user that boards are attached. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['board'],
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
				resource: ['board'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 200,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
