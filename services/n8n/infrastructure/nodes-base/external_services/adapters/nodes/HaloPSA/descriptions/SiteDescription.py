"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HaloPSA/descriptions/SiteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HaloPSA/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:siteOperations、siteFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HaloPSA/descriptions/SiteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HaloPSA/descriptions/SiteDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const siteOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['site'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a site',
				action: 'Create a site',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a site',
				action: 'Delete a site',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a site',
				action: 'Get a site',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many sites',
				action: 'Get many sites',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a site',
				action: 'Update a site',
			},
		],
		default: 'create',
	},
];

export const siteFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                site:create                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'siteName',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['create'],
			},
		},
		description: 'Enter site name',
	},
	{
		displayName: 'Select Client by ID',
		name: 'selectOption',
		type: 'boolean',
		default: false,
		description: 'Whether client can be selected by ID',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Client ID',
		name: 'clientId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['create'],
				selectOption: [true],
			},
		},
	},
	{
		displayName: 'Client Name or ID',
		name: 'clientId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		default: '',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getHaloPSAClients',
		},
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['create'],
				selectOption: [false],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Main Contact',
				name: 'maincontact_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Notes',
				name: 'notes',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Phone Number',
				name: 'phonenumber',
				type: 'string',
				default: '',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                site:get                                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Site ID',
		name: 'siteId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['delete', 'get'],
			},
		},
	},
	{
		displayName: 'Simplify',
		name: 'simplify',
		type: 'boolean',
		default: true,
		description: 'Whether to return a simplified version of the response instead of the raw data',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['get', 'getAll'],
			},
		},
	},
	/* -------------------------------------------------------------------------- */
	/*                                site:getAll                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['getAll'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		description: 'Max number of results to return',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Active Status',
				name: 'activeStatus',
				type: 'options',
				default: 'all',
				options: [
					{
						name: 'Active Only',
						value: 'active',
						description: 'Whether to include active sites in the response',
					},
					{
						name: 'All',
						value: 'all',
						description: 'Whether to include active and inactive sites in the response',
					},
					{
						name: 'Inactive Only',
						value: 'inactive',
						description: 'Whether to include inactive sites in the response',
					},
				],
			},
			{
				displayName: 'Text To Filter By',
				name: 'search',
				type: 'string',
				default: '',
				description: 'Filter sites by your search string',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                site:update                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Site ID',
		name: 'siteId',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['site'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Client ID',
				name: 'client_id',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Main Contact',
				name: 'maincontact_name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Enter site name',
			},
			{
				displayName: 'Notes',
				name: 'notes',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Phone Number',
				name: 'phonenumber',
				type: 'string',
				default: '',
			},
		],
	},
];
