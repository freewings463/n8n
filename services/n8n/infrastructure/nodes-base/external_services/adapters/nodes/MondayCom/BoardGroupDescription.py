"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MondayCom/BoardGroupDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MondayCom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:boardGroupOperations、boardGroupFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MondayCom/BoardGroupDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MondayCom/BoardGroupDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const boardGroupOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['boardGroup'],
			},
		},
		options: [
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a group in a board',
				action: 'Delete a board group',
			},
			{
				name: 'Create',
				value: 'create',
				description: 'Create a group in a board',
				action: 'Create a board group',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get list of groups in a board',
				action: 'Get many board groups',
			},
		],
		default: 'create',
	},
];

export const boardGroupFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 boardGroup:create                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Board Name or ID',
		name: 'boardId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getBoards',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['boardGroup'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['boardGroup'],
			},
		},
		default: '',
		description: 'The group name',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 boardGroup:delete                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Board Name or ID',
		name: 'boardId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getBoards',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['boardGroup'],
				operation: ['delete'],
			},
		},
	},
	{
		displayName: 'Group Name or ID',
		name: 'groupId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getGroups',
			loadOptionsDependsOn: ['boardId'],
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['boardGroup'],
				operation: ['delete'],
			},
		},
	},
	/* -------------------------------------------------------------------------- */
	/*                                 boardGroup:getAll                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Board Name or ID',
		name: 'boardId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getBoards',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['boardGroup'],
				operation: ['getAll'],
			},
		},
	},
];
