"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshservice/descriptions/LocationDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshservice/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:locationOperations、locationFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshservice/descriptions/LocationDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshservice/descriptions/LocationDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const locationOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['location'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a location',
				action: 'Create a location',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a location',
				action: 'Delete a location',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a location',
				action: 'Get a location',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many locations',
				action: 'Get many locations',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a location',
				action: 'Update a location',
			},
		],
		default: 'create',
	},
];

export const locationFields: INodeProperties[] = [
	// ----------------------------------------
	//             location: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		description: 'Name of the location',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['location'],
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
				resource: ['location'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Address',
				name: 'address',
				placeholder: 'Add Address Fields',
				type: 'fixedCollection',
				default: {},
				options: [
					{
						displayName: 'Address Details',
						name: 'addressFields',
						values: [
							{
								displayName: 'Line 1',
								name: 'line1',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Line 2',
								name: 'line2',
								type: 'string',
								default: '',
							},
							{
								displayName: 'City',
								name: 'city',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Country',
								name: 'country',
								type: 'string',
								default: '',
							},
							{
								displayName: 'State',
								name: 'state',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Zip Code',
								name: 'zipcode',
								type: 'string',
								default: '',
							},
						],
					},
				],
			},
		],
	},

	// ----------------------------------------
	//             location: delete
	// ----------------------------------------
	{
		displayName: 'Location ID',
		name: 'locationId',
		description: 'ID of the location to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['location'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//              location: get
	// ----------------------------------------
	{
		displayName: 'Location ID',
		name: 'locationId',
		description: 'ID of the location to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['location'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//             location: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['location'],
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
				resource: ['location'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//             location: update
	// ----------------------------------------
	{
		displayName: 'Location ID',
		name: 'locationId',
		description: 'ID of the location to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['location'],
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
				resource: ['location'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Address',
				name: 'address',
				placeholder: 'Add Address Fields',
				type: 'fixedCollection',
				default: {},
				options: [
					{
						displayName: 'Address Details',
						name: 'addressFields',
						values: [
							{
								displayName: 'Line 1',
								name: 'line1',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Line 2',
								name: 'line2',
								type: 'string',
								default: '',
							},
							{
								displayName: 'City',
								name: 'city',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Country',
								name: 'country',
								type: 'string',
								default: '',
							},
							{
								displayName: 'State',
								name: 'state',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Zip Code',
								name: 'zipcode',
								type: 'string',
								default: '',
							},
						],
					},
				],
			},
		],
	},
];
