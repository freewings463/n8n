"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshservice/descriptions/RequesterDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshservice/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../constants。导出:requesterOperations、requesterFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshservice/descriptions/RequesterDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshservice/descriptions/RequesterDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { LANGUAGES } from '../constants';

export const requesterOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['requester'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a requester',
				action: 'Create a requester',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a requester',
				action: 'Delete a requester',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a requester',
				action: 'Get a requester',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many requesters',
				action: 'Get many requesters',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a requester',
				action: 'Update a requester',
			},
		],
		default: 'create',
	},
];

export const requesterFields: INodeProperties[] = [
	// ----------------------------------------
	//            requester: create
	// ----------------------------------------
	{
		displayName: 'First Name',
		name: 'firstName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requester'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Primary Email',
		name: 'primaryEmail',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['requester'],
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
				resource: ['requester'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Address',
				name: 'address',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Background Information',
				name: 'background_information',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Department Names or IDs',
				name: 'department_ids',
				type: 'multiOptions',
				default: [],
				description:
					'Comma-separated IDs of the departments associated with the requester. Choose from the list or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
				typeOptions: {
					loadOptionsMethod: 'getDepartments',
				},
			},
			{
				displayName: 'Job Title',
				name: 'job_title',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Language',
				name: 'language',
				type: 'options',
				default: '',
				options: LANGUAGES,
			},
			{
				displayName: 'Last Name',
				name: 'last_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Location Name or ID',
				name: 'location_id',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				type: 'options',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getLocations',
				},
			},
			{
				displayName: 'Mobile Phone',
				name: 'mobile_phone_number',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Secondary Emails',
				name: 'secondary_emails',
				type: 'string',
				default: '',
				description: 'Comma-separated secondary emails associated with the requester',
			},
			{
				displayName: 'Time Format',
				name: 'time_format',
				type: 'options',
				default: '12h',
				options: [
					{
						name: '12-Hour Format',
						value: '12h',
					},
					{
						name: '24-Hour Format',
						value: '24h',
					},
				],
			},
			{
				displayName: 'Work Phone',
				name: 'work_phone_number',
				type: 'string',
				default: '',
			},
		],
	},

	// ----------------------------------------
	//            requester: delete
	// ----------------------------------------
	{
		displayName: 'Requester ID',
		name: 'requesterId',
		description: 'ID of the requester to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requester'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//              requester: get
	// ----------------------------------------
	{
		displayName: 'Requester ID',
		name: 'requesterId',
		description: 'ID of the requester to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requester'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//            requester: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['requester'],
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
				resource: ['requester'],
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
				resource: ['requester'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Department Name or ID',
				name: 'department_id',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				type: 'options',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getDepartments',
				},
			},
			{
				displayName: 'First Name',
				name: 'first_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Job Title',
				name: 'job_title',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Language',
				name: 'language',
				type: 'options',
				default: '',
				options: LANGUAGES,
			},
			{
				displayName: 'Last Name',
				name: 'last_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Location Name or ID',
				name: 'location_id',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getLocations',
				},
			},
			{
				displayName: 'Mobile Phone Number',
				name: 'mobile_phone_number',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Primary Email',
				name: 'primary_email',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Work Phone Number',
				name: 'work_phone_number',
				type: 'string',
				default: '',
			},
		],
	},

	// ----------------------------------------
	//            requester: update
	// ----------------------------------------
	{
		displayName: 'Requester ID',
		name: 'requesterId',
		description: 'ID of the requester to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requester'],
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
				resource: ['requester'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Address',
				name: 'address',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Background Information',
				name: 'background_information',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Department Names or IDs',
				name: 'department_ids',
				type: 'multiOptions',
				default: [],
				description:
					'Comma-separated IDs of the departments associated with the requester. Choose from the list or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
				typeOptions: {
					loadOptionsMethod: 'getDepartments',
				},
			},
			{
				displayName: 'First Name',
				name: 'first_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Job Title',
				name: 'job_title',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Language',
				name: 'language',
				type: 'options',
				default: '',
				options: LANGUAGES,
			},
			{
				displayName: 'Last Name',
				name: 'last_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Location Name or ID',
				name: 'location_id',
				type: 'options',
				default: '',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				typeOptions: {
					loadOptionsMethod: 'getLocations',
				},
			},
			{
				displayName: 'Mobile Phone',
				name: 'mobile_phone_number',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Primary Email',
				name: 'primary_email',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Secondary Emails',
				name: 'secondary_emails',
				type: 'string',
				default: '',
				description: 'Comma-separated secondary emails associated with the requester',
			},
			{
				displayName: 'Time Format',
				name: 'time_format',
				type: 'options',
				default: '12h',
				options: [
					{
						name: '12-Hour Format',
						value: '12h',
					},
					{
						name: '24-Hour Format',
						value: '24h',
					},
				],
			},
			{
				displayName: 'Work Phone',
				name: 'work_phone_number',
				type: 'string',
				default: '',
			},
		],
	},
];
