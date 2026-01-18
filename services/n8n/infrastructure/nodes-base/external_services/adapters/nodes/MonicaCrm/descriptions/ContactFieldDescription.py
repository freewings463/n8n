"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MonicaCrm/descriptions/ContactFieldDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MonicaCrm/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactFieldOperations、contactFieldFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MonicaCrm/descriptions/ContactFieldDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MonicaCrm/descriptions/ContactFieldDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const contactFieldOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['contactField'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a contact field',
				action: 'Create a contact field',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a contact field',
				action: 'Delete a contact field',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a contact field',
				action: 'Get a contact field',
			},
			// {
			// 	name: 'Get All',
			// 	value: 'getAll',
			// 	description: 'Retrieve all contact fields',
			// },
			{
				name: 'Update',
				value: 'update',
				description: 'Update a contact field',
				action: 'Update a contact field',
			},
		],
		default: 'create',
	},
];

export const contactFieldFields: INodeProperties[] = [
	// ----------------------------------------
	//           contactField: create
	// ----------------------------------------
	{
		displayName: 'Contact ID',
		name: 'contactId',
		description: 'ID of the contact to associate the contact field with',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Contact Field Type Name or ID',
		name: 'contactFieldTypeId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getContactFieldTypes',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Content',
		name: 'data',
		description: 'Content of the contact field - max 255 characters',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['create'],
			},
		},
	},

	// ----------------------------------------
	//           contactField: delete
	// ----------------------------------------
	{
		displayName: 'Contact Field ID',
		name: 'contactFieldId',
		description: 'ID of the contactField to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//            contactField: get
	// ----------------------------------------
	{
		displayName: 'Contact Field ID',
		name: 'contactFieldId',
		description: 'ID of the contact field to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//           contactField: getAll
	// ----------------------------------------
	{
		displayName: 'Contact ID',
		name: 'contactId',
		description: 'ID of the contact whose fields to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['contactField'],
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
				resource: ['contactField'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//           contactField: update
	// ----------------------------------------
	{
		displayName: 'Contact ID',
		name: 'contactId',
		description: 'ID of the contact to associate the contact field with',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Contact Field ID',
		name: 'contactFieldId',
		description: 'ID of the contact field to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Contact Field Type Name or ID',
		name: 'contactFieldTypeId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getContactFieldTypes',
		},
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Content',
		name: 'data',
		description: 'Content of the contact field - max 255 characters',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactField'],
				operation: ['update'],
			},
		},
	},
];
