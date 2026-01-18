"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshservice/descriptions/DepartmentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshservice/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:departmentOperations、departmentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshservice/descriptions/DepartmentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshservice/descriptions/DepartmentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const departmentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['department'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a department',
				action: 'Create a department',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a department',
				action: 'Delete a department',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a department',
				action: 'Get a department',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many departments',
				action: 'Get many departments',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a department',
				action: 'Update a department',
			},
		],
		default: 'create',
	},
];

export const departmentFields: INodeProperties[] = [
	// ----------------------------------------
	//            department: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['department'],
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
				resource: ['department'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Domains',
				name: 'domains',
				type: 'string',
				default: '',
				description: 'Comma-separated email domains associated with the department',
			},
		],
	},

	// ----------------------------------------
	//            department: delete
	// ----------------------------------------
	{
		displayName: 'Department ID',
		name: 'departmentId',
		description: 'ID of the department to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['department'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//             department: get
	// ----------------------------------------
	{
		displayName: 'Department ID',
		name: 'departmentId',
		description: 'ID of the department to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['department'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//            department: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['department'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['department'],
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
		displayOptions: {
			show: {
				resource: ['department'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name of the department',
			},
		],
	},

	// ----------------------------------------
	//            department: update
	// ----------------------------------------
	{
		displayName: 'Department ID',
		name: 'departmentId',
		description: 'ID of the department to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['department'],
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
				resource: ['department'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Domains',
				name: 'domains',
				type: 'string',
				default: '',
				description: 'Comma-separated email domains associated with the department',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
		],
	},
];
