"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBooks/descriptions/Employee/EmployeeDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBooks/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./EmployeeAdditionalFieldsOptions。导出:employeeOperations、employeeFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBooks/descriptions/Employee/EmployeeDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBooks/descriptions/Employee/EmployeeDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { employeeAdditionalFieldsOptions } from './EmployeeAdditionalFieldsOptions';

export const employeeOperations: INodeProperties[] = [
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
				action: 'Create an employee',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an employee',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many employees',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update an employee',
			},
		],
		displayOptions: {
			show: {
				resource: ['employee'],
			},
		},
	},
];

export const employeeFields: INodeProperties[] = [
	// ----------------------------------
	//         employee: create
	// ----------------------------------
	{
		displayName: 'Family Name',
		name: 'FamilyName',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['employee'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Given Name',
		name: 'GivenName',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['employee'],
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
				resource: ['employee'],
				operation: ['create'],
			},
		},
		options: employeeAdditionalFieldsOptions,
	},

	// ----------------------------------
	//         employee: get
	// ----------------------------------
	{
		displayName: 'Employee ID',
		name: 'employeeId',
		type: 'string',
		required: true,
		default: '',
		description: 'The ID of the employee to retrieve',
		displayOptions: {
			show: {
				resource: ['employee'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//         employee: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['employee'],
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
			maxValue: 1000,
		},
		displayOptions: {
			show: {
				resource: ['employee'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Query',
				name: 'query',
				type: 'string',
				default: '',
				placeholder: "WHERE Metadata.LastUpdatedTime > '2021-01-01'",
				description:
					'The condition for selecting employees. See the <a href="https://developer.intuit.com/app/developer/qbo/docs/develop/explore-the-quickbooks-online-api/data-queries">guide</a> for supported syntax.',
			},
		],
		displayOptions: {
			show: {
				resource: ['employee'],
				operation: ['getAll'],
			},
		},
	},

	// ----------------------------------
	//         employee: update
	// ----------------------------------
	{
		displayName: 'Employee ID',
		name: 'employeeId',
		type: 'string',
		required: true,
		default: '',
		description: 'The ID of the employee to update',
		displayOptions: {
			show: {
				resource: ['employee'],
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
		required: true,
		displayOptions: {
			show: {
				resource: ['employee'],
				operation: ['update'],
			},
		},
		options: employeeAdditionalFieldsOptions,
	},
];
