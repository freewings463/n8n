"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wekan/ChecklistDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wekan 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:checklistOperations、checklistFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wekan/ChecklistDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wekan/ChecklistDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const checklistOperations: INodeProperties[] = [
	// ----------------------------------
	//         checklist
	// ----------------------------------
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['checklist'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new checklist',
				action: 'Create a checklist',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a checklist',
				action: 'Delete a checklist',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get the data of a checklist',
				action: 'Get a checklist',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Returns many checklists for the card',
				action: 'Get many checklists',
			},
		],
		default: 'getAll',
	},
];

export const checklistFields: INodeProperties[] = [
	// ----------------------------------
	//         checklist:create
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
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the board where the card is in. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
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
				resource: ['checklist'],
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
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the card to add checklist to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['checklist'],
			},
		},
		description: 'The title of the checklist to add',
	},
	{
		displayName: 'Items',
		name: 'items',
		type: 'string',
		typeOptions: {
			multipleValues: true,
			multipleValueButtonText: 'Add Item',
		},
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['checklist'],
			},
		},
		default: [],
		description: 'Items to be added to the checklist',
	},

	// ----------------------------------
	//         checklist:delete
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
				resource: ['checklist'],
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
				resource: ['checklist'],
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
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the card that checklist belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Checklist Name or ID',
		name: 'checklistId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getChecklists',
			loadOptionsDependsOn: ['boardId', 'cardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the checklist to delete. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},

	// ----------------------------------
	//         checklist:get
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
				operation: ['get'],
				resource: ['checklist'],
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
				operation: ['get'],
				resource: ['checklist'],
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
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the card that checklist belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Checklist Name or ID',
		name: 'checklistId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getChecklists',
			loadOptionsDependsOn: ['boardId', 'cardId'],
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the checklist to get. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},

	// ----------------------------------
	//         checklist:getAll
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
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the board that list belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
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
				resource: ['checklist'],
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
				resource: ['checklist'],
			},
		},
		description:
			'The ID of the card to get checklists. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['checklist'],
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
				resource: ['checklist'],
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
