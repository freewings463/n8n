"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MondayCom/BoardColumnDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MondayCom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:boardColumnOperations、boardColumnFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MondayCom/BoardColumnDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MondayCom/BoardColumnDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const boardColumnOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['boardColumn'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new column',
				action: 'Create a board column',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many columns',
				action: 'Get many board columns',
			},
		],
		default: 'create',
	},
];

export const boardColumnFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 boardColumn:create                         */
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
				resource: ['boardColumn'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['boardColumn'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Column Type',
		name: 'columnType',
		type: 'options',
		default: '',
		options: [
			{
				name: 'Checkbox',
				value: 'checkbox',
			},
			{
				name: 'Country',
				value: 'country',
			},
			{
				name: 'Date',
				value: 'date',
			},
			{
				name: 'Dropdown',
				value: 'dropdown',
			},
			{
				name: 'Email',
				value: 'email',
			},
			{
				name: 'Hour',
				value: 'hour',
			},
			{
				name: 'Link',
				value: 'Link',
			},
			{
				name: 'Long Text',
				value: 'longText',
			},
			{
				name: 'Numbers',
				value: 'numbers',
			},
			{
				name: 'People',
				value: 'people',
			},
			{
				name: 'Person',
				value: 'person',
			},
			{
				name: 'Phone',
				value: 'phone',
			},
			{
				name: 'Rating',
				value: 'rating',
			},
			{
				name: 'Status',
				value: 'status',
			},
			{
				name: 'Tags',
				value: 'tags',
			},
			{
				name: 'Team',
				value: 'team',
			},
			{
				name: 'Text',
				value: 'text',
			},
			{
				name: 'Timeline',
				value: 'timeline',
			},
			{
				name: 'Timezone',
				value: 'timezone',
			},
			{
				name: 'Week',
				value: 'week',
			},
			{
				name: 'World Clock',
				value: 'worldClock',
			},
		],
		required: true,
		displayOptions: {
			show: {
				resource: ['boardColumn'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['boardColumn'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Defauls',
				name: 'defaults',
				type: 'json',
				typeOptions: {
					alwaysOpenEditWindow: true,
				},
				default: '',
				description: "The new column's defaults",
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                 boardColumn:getAll                         */
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
				resource: ['boardColumn'],
				operation: ['getAll'],
			},
		},
	},
];
