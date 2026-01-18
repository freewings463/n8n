"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHive/descriptions/TaskDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHive/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:taskOperations、taskFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHive/descriptions/TaskDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHive/descriptions/TaskDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const taskOperations: INodeProperties[] = [
	{
		displayName: 'Operation Name or ID',
		name: 'operation',
		default: 'getAll',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		noDataExpression: true,
		required: true,
		displayOptions: {
			show: {
				resource: ['task'],
			},
		},
		typeOptions: {
			loadOptionsDependsOn: ['operation'],
			loadOptionsMethod: 'loadTaskOptions',
		},
	},
];

export const taskFields: INodeProperties[] = [
	{
		displayName: 'Task ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['update', 'executeResponder', 'get'],
			},
		},
		description: 'ID of the taks',
	},
	{
		displayName: 'Case ID',
		name: 'caseId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['create', 'getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['search', 'getAll'],
				resource: ['task'],
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
				operation: ['search', 'getAll'],
				resource: ['task'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['create'],
			},
		},
		description: 'Task details',
	},
	{
		displayName: 'Status',
		name: 'status',
		type: 'options',
		default: 'Waiting',
		options: [
			{
				name: 'Cancel',
				value: 'Cancel',
			},
			{
				name: 'Completed',
				value: 'Completed',
			},
			{
				name: 'InProgress',
				value: 'InProgress',
			},
			{
				name: 'Waiting',
				value: 'Waiting',
			},
		],
		required: true,
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['create'],
			},
		},
		description: 'Status of the task. Default=Waiting.',
	},
	{
		displayName: 'Flag',
		name: 'flag',
		type: 'boolean',
		required: true,
		default: false,
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['create'],
			},
		},
		description: 'Whether to flag the task. Default=false.',
	},
	// required for responder execution
	{
		displayName: 'Responder Name or ID',
		name: 'responder',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsDependsOn: ['id'],
			loadOptionsMethod: 'loadResponders',
		},
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['executeResponder'],
			},
			hide: {
				id: [''],
			},
		},
	},
	// optional attributes (Create operations)
	{
		displayName: 'Options',
		type: 'collection',
		name: 'options',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Task details',
			},
			{
				displayName: 'End Date',
				name: 'endDate',
				type: 'dateTime',
				default: '',
				description:
					'Date of the end of the task. This is automatically set when status is set to Completed.',
			},
			{
				displayName: 'Owner',
				name: 'owner',
				type: 'string',
				default: '',
				description:
					'User who owns the task. This is automatically set to current user when status is set to InProgress.',
			},
			{
				displayName: 'Start Date',
				name: 'startDate',
				type: 'dateTime',
				default: '',
				description:
					'Date of the beginning of the task. This is automatically set when status is set to Open.',
			},
		],
	},
	// optional attributes (Update operation)

	{
		displayName: 'Update Fields',
		type: 'collection',
		name: 'updateFields',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Task details',
			},
			{
				displayName: 'End Date',
				name: 'endDate',
				type: 'dateTime',
				default: '',
				description:
					'Date of the end of the task. This is automatically set when status is set to Completed.',
			},
			{
				displayName: 'Flag',
				name: 'flag',
				type: 'boolean',
				default: false,
				description: 'Whether to flag the task. Default=false.',
			},
			{
				displayName: 'Owner',
				name: 'owner',
				type: 'string',
				default: '',
				description:
					'User who owns the task. This is automatically set to current user when status is set to InProgress.',
			},
			{
				displayName: 'Start Date',
				name: 'startDate',
				type: 'dateTime',
				default: '',
				description:
					'Date of the beginning of the task. This is automatically set when status is set to Open.',
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				default: 'Waiting',
				options: [
					{
						name: 'Cancel',
						value: 'Cancel',
					},
					{
						name: 'Completed',
						value: 'Completed',
					},
					{
						name: 'In Progress',
						value: 'InProgress',
					},
					{
						name: 'Waiting',
						value: 'Waiting',
					},
				],
				description: 'Status of the task. Default=Waiting.',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Task details',
			},
		],
	},

	// query options
	{
		displayName: 'Options',
		name: 'options',
		placeholder: 'Add option',
		type: 'collection',
		default: {},
		displayOptions: {
			show: {
				operation: ['getAll', 'search'],
				resource: ['task'],
			},
		},
		options: [
			{
				displayName: 'Sort',
				name: 'sort',
				type: 'string',
				placeholder: '±Attribut, exp +status',
				description: 'Specify the sorting attribut, + for asc, - for desc',
				default: '',
			},
		],
	},
	// query attributes
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		default: {},
		placeholder: 'Add Filter',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['search', 'count'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Task details',
			},
			{
				displayName: 'End Date',
				name: 'endDate',
				type: 'dateTime',
				default: '',
				description:
					'Date of the end of the task. This is automatically set when status is set to Completed.',
			},
			{
				displayName: 'Flag',
				name: 'flag',
				type: 'boolean',
				default: false,
				description: 'Whether to flag the task. Default=false.',
			},
			{
				displayName: 'Owner',
				name: 'owner',
				type: 'string',
				default: '',
				description:
					'User who owns the task. This is automatically set to current user when status is set to InProgress.',
			},
			{
				displayName: 'Start Date',
				name: 'startDate',
				type: 'dateTime',
				default: '',
				description:
					'Date of the beginning of the task. This is automatically set when status is set to Open.',
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				default: 'Waiting',
				options: [
					{
						name: 'Cancel',
						value: 'Cancel',
					},
					{
						name: 'Completed',
						value: 'Completed',
					},
					{
						name: 'In Progress',
						value: 'InProgress',
					},
					{
						name: 'Waiting',
						value: 'Waiting',
					},
				],
				description: 'Status of the task. Default=Waiting.',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Task details',
			},
		],
	},
];
