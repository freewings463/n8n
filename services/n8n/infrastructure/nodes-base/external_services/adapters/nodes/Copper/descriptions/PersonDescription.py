"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Copper/descriptions/PersonDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Copper/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:personOperations、personFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Copper/descriptions/PersonDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Copper/descriptions/PersonDescription.py

import type { INodeProperties } from 'n8n-workflow';

import {
	addressFixedCollection,
	emailsFixedCollection,
	phoneNumbersFixedCollection,
} from '../utils/sharedFields';

export const personOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['person'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a person',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a person',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a person',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many people',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a person',
			},
		],
		default: 'create',
	},
];

export const personFields: INodeProperties[] = [
	// ----------------------------------------
	//              person: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		description: 'Name of the person to create',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
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
				resource: ['person'],
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
				description: 'Description to set for the person',
			},
			{
				displayName: 'Email Domain',
				name: 'email_domain',
				type: 'string',
				default: '',
			},
			emailsFixedCollection,
			phoneNumbersFixedCollection,
		],
	},

	// ----------------------------------------
	//              person: delete
	// ----------------------------------------
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//               person: get
	// ----------------------------------------
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//              person: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['person'],
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
				resource: ['person'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filterFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name of the person to filter by',
			},
		],
	},

	// ----------------------------------------
	//              person: update
	// ----------------------------------------
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
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
				resource: ['person'],
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
				description: 'Description to set for the person',
			},
			{
				displayName: 'Email Domain',
				name: 'email_domain',
				type: 'string',
				default: '',
			},
			emailsFixedCollection,
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name to set for the person',
			},
			phoneNumbersFixedCollection,
		],
	},
];
