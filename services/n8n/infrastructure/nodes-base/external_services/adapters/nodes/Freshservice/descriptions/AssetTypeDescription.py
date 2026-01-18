"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshservice/descriptions/AssetTypeDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshservice/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:assetTypeOperations、assetTypeFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshservice/descriptions/AssetTypeDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshservice/descriptions/AssetTypeDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const assetTypeOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['assetType'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an asset type',
				action: 'Create an asset type',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an asset type',
				action: 'Delete an asset type',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve an asset type',
				action: 'Get an asset type',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many asset types',
				action: 'Get many asset types',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an asset type',
				action: 'Update an asset type',
			},
		],
		default: 'create',
	},
];

export const assetTypeFields: INodeProperties[] = [
	// ----------------------------------------
	//            assetType: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['assetType'],
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
				resource: ['assetType'],
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
				displayName: 'Parent Asset Type Name or ID',
				name: 'parent_asset_type_id',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				type: 'options',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getAssetTypes',
				},
			},
		],
	},

	// ----------------------------------------
	//            assetType: delete
	// ----------------------------------------
	{
		displayName: 'Asset Type ID',
		name: 'assetTypeId',
		description: 'ID of the asset type to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['assetType'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//              assetType: get
	// ----------------------------------------
	{
		displayName: 'Asset Type ID',
		name: 'assetTypeId',
		description: 'ID of the asset type to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['assetType'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//            assetType: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['assetType'],
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
				resource: ['assetType'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//            assetType: update
	// ----------------------------------------
	{
		displayName: 'Asset Type ID',
		name: 'assetTypeId',
		description: 'ID of the asset type to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['assetType'],
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
				resource: ['assetType'],
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
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
		],
	},
];
