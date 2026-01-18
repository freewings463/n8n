"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Copper/descriptions/CompanyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Copper/descriptions 的节点。导入/依赖:外部:@utils/ISOCountryCodes；内部:n8n-workflow；本地:../utils/sharedFields。导出:companyOperations、companyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Copper/descriptions/CompanyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Copper/descriptions/CompanyDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { isoCountryCodes } from '@utils/ISOCountryCodes';

import { addressFixedCollection, phoneNumbersFixedCollection } from '../utils/sharedFields';

export const companyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['company'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a company',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a company',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a company',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many companies',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a company',
			},
		],
		default: 'create',
	},
];

export const companyFields: INodeProperties[] = [
	// ----------------------------------------
	//             company: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		description: 'Name of the company to create',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['company'],
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
				resource: ['company'],
				operation: ['create'],
			},
		},
		options: [
			addressFixedCollection,
			{
				displayName: 'Details',
				name: 'details',
				type: 'string',
				default: '',
				description: 'Description of the company to create',
			},
			{
				displayName: 'Email Domain',
				name: 'email_domain',
				type: 'string',
				default: '',
			},
			phoneNumbersFixedCollection,
		],
	},

	// ----------------------------------------
	//             company: delete
	// ----------------------------------------
	{
		displayName: 'Company ID',
		name: 'companyId',
		description: 'ID of the company to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//               company: get
	// ----------------------------------------
	{
		displayName: 'Company ID',
		name: 'companyId',
		description: 'ID of the company to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//             company: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['company'],
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
				resource: ['company'],
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
				resource: ['company'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Country',
				name: 'country',
				type: 'options',
				options: isoCountryCodes.map(({ name, alpha2 }) => ({ name, value: alpha2 })),
				default: '',
				description: 'Country of the company to filter by',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name of the company to filter by',
			},
		],
	},

	// ----------------------------------------
	//             company: update
	// ----------------------------------------
	{
		displayName: 'Company ID',
		name: 'companyId',
		description: 'ID of the company to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['company'],
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
				resource: ['company'],
				operation: ['update'],
			},
		},
		options: [
			addressFixedCollection,
			{
				displayName: 'Details',
				name: 'details',
				type: 'string',
				default: '',
				description: 'Description to set for the company',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name to set for the company',
			},
			phoneNumbersFixedCollection,
		],
	},
];
