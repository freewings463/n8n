"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/ToDo/LinkedResourceDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/ToDo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:linkedResourceOperations、linkedResourceFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/ToDo/LinkedResourceDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/ToDo/LinkedResourceDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const linkedResourceOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['linkedResource'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a linked resource',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a linked resource',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a linked resource',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many linked resources',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a linked resource',
			},
		],
		default: 'get',
	},
];

export const linkedResourceFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                       linkedResource:ALL                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Task List Name or ID',
		name: 'taskListId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getTaskLists',
		},
		displayOptions: {
			show: {
				operation: ['create', 'delete', 'get', 'getAll', 'update'],
				resource: ['linkedResource'],
			},
		},
		required: true,
		default: '',
	},
	{
		displayName: 'Task ID',
		name: 'taskId',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['create', 'delete', 'get', 'getAll', 'update'],
				resource: ['linkedResource'],
			},
		},
		required: true,
		default: '',
	},

	/* -------------------------------------------------------------------------- */
	/*                           linkedResource:create                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'displayName',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['linkedResource'],
			},
		},
		description: 'Field indicating title of the linked entity',
	},
	{
		displayName: 'Application Name',
		name: 'applicationName',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['linkedResource'],
			},
		},
		required: true,
		default: '',
		description: 'App name of the source that is sending the linked entity',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['linkedResource'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'External ID',
				name: 'externalId',
				type: 'string',
				default: '',
				description:
					'ID of the object that is associated with this task on the third-party/partner system',
			},
			{
				displayName: 'Web URL',
				name: 'webUrl',
				type: 'string',
				default: '',
				description: 'Deeplink to the linked entity',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                           linkedResource:get/delete/update                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Linked Resource ID',
		name: 'linkedResourceId',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['linkedResource'],
				operation: ['delete', 'get', 'update'],
			},
		},
		default: '',
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                           linkedResource:getAll                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['linkedResource'],
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
				resource: ['linkedResource'],
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
	/*                           linkedResource:update                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['linkedResource'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Application Name',
				name: 'applicationName',
				type: 'string',
				default: '',
				description: 'App name of the source that is sending the linked entity',
			},
			{
				displayName: 'Name',
				name: 'displayName',
				type: 'string',
				default: '',
				description: 'Field indicating title of the linked entity',
			},
			{
				displayName: 'External ID',
				name: 'externalId',
				type: 'string',
				default: '',
				description:
					'ID of the object that is associated with this task on the third-party/partner system',
			},
			{
				displayName: 'Web URL',
				name: 'webUrl',
				type: 'string',
				default: '',
				description: 'Deeplink to the linked entity',
			},
		],
	},
];
