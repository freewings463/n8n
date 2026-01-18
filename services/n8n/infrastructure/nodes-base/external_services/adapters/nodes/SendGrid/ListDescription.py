"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SendGrid/ListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SendGrid 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:listOperations、listFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SendGrid/ListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SendGrid/ListDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const listOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['list'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a list',
				action: 'Create a list',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a list',
				action: 'Delete a list',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a list',
				action: 'Get a list',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many lists',
				action: 'Get many lists',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a list',
				action: 'Update a list',
			},
		],
		default: 'create',
	},
];

export const listFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 list:getAll                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['list'],
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
		displayOptions: {
			show: {
				resource: ['list'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		default: 100,
		description: 'Max number of results to return',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 list:create                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['list'],
			},
		},
		default: '',
		description: 'Name of the list',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 list:delete                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['list'],
			},
		},
		default: '',
		description: 'ID of the list',
	},
	{
		displayName: 'Delete Contacts',
		name: 'deleteContacts',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['list'],
			},
		},
		description: 'Whether to delete all contacts on the list',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 list:get                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['list'],
			},
		},
		default: '',
		description: 'ID of the list',
	},
	{
		displayName: 'Contact Sample',
		name: 'contactSample',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['list'],
			},
		},
		description: 'Whether to return the contact sample',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 list:update                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['list'],
			},
		},
		default: '',
		description: 'ID of the list',
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['list'],
			},
		},
		default: '',
		description: 'Name of the list',
	},
];
