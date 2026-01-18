"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Copper/descriptions/ProjectDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Copper/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:projectOperations、projectFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Copper/descriptions/ProjectDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Copper/descriptions/ProjectDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const projectOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['project'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a project',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a project',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a project',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many projects',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a project',
			},
		],
		default: 'create',
	},
];

export const projectFields: INodeProperties[] = [
	// ----------------------------------------
	//             project: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		description: 'Name of the project to create',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
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
				resource: ['project'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Assignee ID',
				name: 'assignee_id',
				type: 'string',
				default: '',
				description: 'ID of the user who will own the project to create',
			},
			{
				displayName: 'Details',
				name: 'details',
				type: 'string',
				default: '',
				description: 'Description of the project to create',
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
	//             project: delete
	// ----------------------------------------
	{
		displayName: 'Project ID',
		name: 'projectId',
		description: 'ID of the project to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//               project: get
	// ----------------------------------------
	{
		displayName: 'Project ID',
		name: 'projectId',
		description: 'ID of the project to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//             project: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['project'],
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
				resource: ['project'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filterFields',
		type: 'collection',
		default: {},
		placeholder: 'Add Filter',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name of the project to filter by',
			},
		],
	},

	// ----------------------------------------
	//             project: update
	// ----------------------------------------
	{
		displayName: 'Project ID',
		name: 'projectId',
		description: 'ID of the project to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
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
				resource: ['project'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Assignee ID',
				name: 'assignee_id',
				type: 'string',
				default: '',
				description: 'ID of the user who will own the project',
			},
			{
				displayName: 'Details',
				name: 'details',
				type: 'string',
				default: '',
				description: 'Description to set for the project',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name to set for the project',
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
