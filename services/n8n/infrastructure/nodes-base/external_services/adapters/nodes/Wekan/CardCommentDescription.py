"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wekan/CardCommentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wekan 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:cardCommentOperations、cardCommentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wekan/CardCommentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wekan/CardCommentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const cardCommentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['cardComment'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a comment on a card',
				action: 'Create a comment on a card',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a comment from a card',
				action: 'Delete a comment from a card',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a card comment',
				action: 'Get a card comment',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many card comments',
				action: 'Get many card comments',
			},
		],
		default: 'create',
	},
];

export const cardCommentFields: INodeProperties[] = [
	// ----------------------------------
	//         cardComment:create
	// ----------------------------------
	{
		displayName: 'Board Name or ID',
		name: 'boardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getBoards',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the board that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'List Name or ID',
		name: 'listId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLists',
			loadOptionsDependsOn: ['boardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the list that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Card Name or ID',
		name: 'cardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getCards',
			loadOptionsDependsOn: ['boardId', 'listId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the card. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Author Name or ID',
		name: 'authorId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['cardComment'],
			},
		},
		description:
			'The user who posted the comment. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Comment',
		name: 'comment',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['cardComment'],
			},
		},
		description: 'The comment text',
	},

	// ----------------------------------
	//         cardComment:delete
	// ----------------------------------
	{
		displayName: 'Board Name or ID',
		name: 'boardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getBoards',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the board that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'List Name or ID',
		name: 'listId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLists',
			loadOptionsDependsOn: ['boardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the list that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Card Name or ID',
		name: 'cardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getCards',
			loadOptionsDependsOn: ['boardId', 'listId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the card. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Comment Name or ID',
		name: 'commentId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getComments',
			loadOptionsDependsOn: ['boardId', 'cardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the comment to delete. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},

	// ----------------------------------
	//         cardComment:get
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
				resource: ['cardComment'],
			},
		},
		description: 'The ID of the board that card belongs to',
	},
	{
		displayName: 'List Name or ID',
		name: 'listId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLists',
			loadOptionsDependsOn: ['boardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the list that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Card Name or ID',
		name: 'cardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getCards',
			loadOptionsDependsOn: ['boardId', 'listId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the card. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Comment ID',
		name: 'commentId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['cardComment'],
			},
		},
		description: 'The ID of the comment to get',
	},

	// ----------------------------------
	//         cardComment:getAll
	// ----------------------------------
	{
		displayName: 'Board Name or ID',
		name: 'boardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getBoards',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the board that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'List Name or ID',
		name: 'listId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLists',
			loadOptionsDependsOn: ['boardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the list that card belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Card Name or ID',
		name: 'cardId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getCards',
			loadOptionsDependsOn: ['boardId', 'listId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['cardComment'],
			},
		},
		description:
			'The ID of the card. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['cardComment'],
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
				resource: ['cardComment'],
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
