"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/ToDo/ListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/ToDo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:listOperations、listFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/ToDo/ListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/ToDo/ListDescription.py

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
				action: 'Create a list',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a list',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a list',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many lists',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a list',
			},
		],
		default: 'get',
	},
];

export const listFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 list:create                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List Name',
		name: 'displayName',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['list'],
			},
		},
		required: true,
		default: '',
		description: 'List display name',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 list:get/delete/update                     */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['delete', 'get', 'update'],
				resource: ['list'],
			},
		},
		required: true,
		default: '',
		description: "The identifier of the list, unique in the user's mailbox",
	},

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
			maxValue: 100,
		},
		default: 50,
		description: 'Max number of results to return',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 list:update                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'New List Name',
		name: 'displayName',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['list'],
			},
		},
		required: true,
		default: '',
		description: 'List display name',
	},
];
