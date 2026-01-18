"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBooks/descriptions/Vendor/VendorDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBooks/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./VendorAdditionalFieldsOptions。导出:vendorOperations、vendorFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBooks/descriptions/Vendor/VendorDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBooks/descriptions/Vendor/VendorDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { vendorAdditionalFieldsOptions } from './VendorAdditionalFieldsOptions';

export const vendorOperations: INodeProperties[] = [
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
				action: 'Create a vendor',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a vendor',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many vendors',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a vendor',
			},
		],
		displayOptions: {
			show: {
				resource: ['vendor'],
			},
		},
	},
];

export const vendorFields: INodeProperties[] = [
	// ----------------------------------
	//         vendor: create
	// ----------------------------------
	{
		displayName: 'Display Name',
		name: 'displayName',
		type: 'string',
		required: true,
		default: '',
		description: 'The display name of the vendor to create',
		displayOptions: {
			show: {
				resource: ['vendor'],
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
				resource: ['vendor'],
				operation: ['create'],
			},
		},
		options: vendorAdditionalFieldsOptions,
	},

	// ----------------------------------
	//         vendor: get
	// ----------------------------------
	{
		displayName: 'Vendor ID',
		name: 'vendorId',
		type: 'string',
		required: true,
		default: '',
		description: 'The ID of the vendor to retrieve',
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//         vendor: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['vendor'],
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
				resource: ['vendor'],
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
					'The condition for selecting vendors. See the <a href="https://developer.intuit.com/app/developer/qbo/docs/develop/explore-the-quickbooks-online-api/data-queries">guide</a> for supported syntax.',
			},
		],
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['getAll'],
			},
		},
	},

	// ----------------------------------
	//         vendor: update
	// ----------------------------------
	{
		displayName: 'Vendor ID',
		name: 'vendorId',
		type: 'string',
		required: true,
		default: '',
		description: 'The ID of the vendor to update',
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
		required: true,
		displayOptions: {
			show: {
				resource: ['vendor'],
				operation: ['update'],
			},
		},
		options: vendorAdditionalFieldsOptions,
	},
];
