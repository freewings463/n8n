"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Copper/descriptions/TaskDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Copper/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:taskOperations、taskFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Copper/descriptions/TaskDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Copper/descriptions/TaskDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const taskOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['task'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a task',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a task',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a task',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many tasks',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a task',
			},
		],
		default: 'create',
	},
];

export const taskFields: INodeProperties[] = [
	// ----------------------------------------
	//               task: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
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
				resource: ['task'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Assignee ID',
				name: 'assignee_id',
				type: 'string',
				default: '',
				description: 'ID of the user who will own the task to create',
			},
			{
				displayName: 'Details',
				name: 'details',
				type: 'string',
				default: '',
				description: 'Description of the task to create',
			},
			{
				displayName: 'Priority',
				name: 'priority',
				type: 'options',
				default: 'High',
				options: [
					{
						name: 'High',
						value: 'High',
					},
					{
						name: 'None',
						value: 'None',
					},
				],
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				default: 'Open',
				options: [
					{
						name: 'Completed',
						value: 'Completed',
					},
					{
						name: 'Open',
						value: 'Open',
					},
				],
			},
		],
	},

	// ----------------------------------------
	//               task: delete
	// ----------------------------------------
	{
		displayName: 'Task ID',
		name: 'taskId',
		description: 'ID of the task to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//                task: get
	// ----------------------------------------
	{
		displayName: 'Task ID',
		name: 'taskId',
		description: 'ID of the task to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//               task: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 5,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filterFields',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['task'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Assignee IDs',
				name: 'assignee_ids',
				type: 'string',
				default: '',
				description: 'Comma-separated IDs of assignee IDs to filter by',
			},
			{
				displayName: 'Project IDs',
				name: 'project_ids',
				type: 'string',
				default: '',
				description: 'Comma-separated IDs of project IDs to filter by',
			},
		],
	},

	// ----------------------------------------
	//               task: update
	// ----------------------------------------
	{
		displayName: 'Task ID',
		name: 'taskId',
		description: 'ID of the task to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['task'],
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
				resource: ['task'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Assignee ID',
				name: 'assignee_id',
				type: 'string',
				default: '',
				description: 'ID of the user who will own the task',
			},
			{
				displayName: 'Details',
				name: 'details',
				type: 'string',
				default: '',
				description: 'Description to set for the task',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name to set for the task',
			},
			{
				displayName: 'Priority',
				name: 'priority',
				type: 'options',
				default: 'High',
				options: [
					{
						name: 'High',
						value: 'High',
					},
					{
						name: 'None',
						value: 'None',
					},
				],
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				default: 'Open',
				options: [
					{
						name: 'Completed',
						value: 'Completed',
					},
					{
						name: 'Open',
						value: 'Open',
					},
				],
			},
		],
	},
];
