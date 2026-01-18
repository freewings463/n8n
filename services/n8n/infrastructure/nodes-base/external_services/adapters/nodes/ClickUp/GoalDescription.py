"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/GoalDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:goalOperations、goalFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/GoalDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/GoalDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const goalOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['goal'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a goal',
				action: 'Create a goal',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a goal',
				action: 'Delete a goal',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a goal',
				action: 'Get a goal',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many goals',
				action: 'Get many goals',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a goal',
				action: 'Update a goal',
			},
		],
		default: 'create',
	},
];

export const goalFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                goal:create                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Team Name or ID',
		name: 'team',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		default: '',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['create'],
			},
		},
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		required: true,
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['create'],
			},
		},
		required: true,
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Color',
				name: 'color',
				type: 'color',
				default: '',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Due Date',
				name: 'dueDate',
				type: 'dateTime',
				default: '',
			},
			{
				displayName: 'Multiple Owners',
				name: 'multipleOwners',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Owners',
				name: 'owners',
				type: 'string',
				default: '',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                goal:delete                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Goal ID',
		name: 'goal',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['delete'],
			},
		},
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                goal:get                                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Goal ID',
		name: 'goal',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['get'],
			},
		},
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                goal:getAll                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Team Name or ID',
		name: 'team',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		default: '',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['getAll'],
			},
		},
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		required: true,
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['getAll'],
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
	/*                                goal:update                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Goal ID',
		name: 'goal',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['update'],
			},
		},
		required: true,
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['goal'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Add Owners',
				name: 'addOwners',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Color',
				name: 'color',
				type: 'color',
				default: '',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Due Date',
				name: 'dueDate',
				type: 'dateTime',
				default: '',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Remove Owners',
				name: 'removeOwners',
				type: 'string',
				default: '',
			},
		],
	},
];
