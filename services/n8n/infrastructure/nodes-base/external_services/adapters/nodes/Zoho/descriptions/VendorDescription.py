"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zoho/descriptions/VendorDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zoho/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:vendorOperations、vendorFields。关键函数/方法:makeCustomFieldsFixedCollection。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zoho/descriptions/VendorDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zoho/descriptions/VendorDescription.py

import type { INodeProperties } from 'n8n-workflow';

import {
	address,
	currencies,
	makeCustomFieldsFixedCollection,
	makeGetAllFields,
} from './SharedFields';

export const vendorOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['vendor'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a vendor',
				action: 'Create a vendor',
			},
			{
				name: 'Create or Update',
				value: 'upsert',
				description: 'Create a new record, or update the current one if it already exists (upsert)',
				action: 'Create or update a vendor',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a vendor',
				action: 'Delete a vendor',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a vendor',
				action: 'Get a vendor',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many vendors',
				action: 'Get many vendors',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a vendor',
				action: 'Update a vendor',
			},
		],
		default: 'create',
	},
];

export const vendorFields: INodeProperties[] = [
	// ----------------------------------------
	//            vendor: create
	// ----------------------------------------
	{
		displayName: 'Vendor Name',
		name: 'vendorName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['create'],
			},
		},
	},

	// ----------------------------------------
	//           vendor: upsert
	// ----------------------------------------
	{
		displayName: 'Vendor Name',
		name: 'vendorName',
		description:
			'Name of the vendor. If a record with this vendor name exists it will be updated, otherwise a new one will be created.',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['upsert'],
			},
		},
	},

	// ----------------------------------------
	//         vendor: create + upsert
	// ----------------------------------------
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['create', 'upsert'],
			},
		},
		options: [
			address,
			{
				displayName: 'Category',
				name: 'Category',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Currency',
				name: 'Currency',
				type: 'options',
				default: 'USD',
				options: currencies,
			},
			makeCustomFieldsFixedCollection('vendor'),
			{
				displayName: 'Description',
				name: 'Description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Email',
				name: 'Email',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Phone',
				name: 'Phone',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Website',
				name: 'Website',
				type: 'string',
				default: '',
			},
		],
	},

	// ----------------------------------------
	//             vendor: delete
	// ----------------------------------------
	{
		displayName: 'Vendor ID',
		name: 'vendorId',
		description: 'ID of the vendor to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//               vendor: get
	// ----------------------------------------
	{
		displayName: 'Vendor ID',
		name: 'vendorId',
		description: 'ID of the vendor to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//             vendor: getAll
	// ----------------------------------------
	...makeGetAllFields('vendor'),

	// ----------------------------------------
	//             vendor: update
	// ----------------------------------------
	{
		displayName: 'Vendor ID',
		name: 'vendorId',
		description: 'ID of the vendor to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['vendor'],
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
				resource: ['vendor'],
				operation: ['update'],
			},
		},
		options: [
			address,
			{
				displayName: 'Category',
				name: 'Category',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Currency',
				name: 'Currency',
				type: 'string',
				default: '',
			},
			makeCustomFieldsFixedCollection('vendor'),
			{
				displayName: 'Description',
				name: 'Description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Email',
				name: 'Email',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Phone',
				name: 'Phone',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Vendor Name',
				name: 'Vendor_Name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Website',
				name: 'Website',
				type: 'string',
				default: '',
			},
		],
	},
];
