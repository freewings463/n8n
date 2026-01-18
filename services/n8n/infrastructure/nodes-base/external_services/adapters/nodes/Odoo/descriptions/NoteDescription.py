"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Odoo/descriptions/NoteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Odoo/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:noteOperations、noteDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Odoo/descriptions/NoteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Odoo/descriptions/NoteDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const noteOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		default: 'create',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['note'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new note',
				action: 'Create a note',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a note',
				action: 'Delete a note',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a note',
				action: 'Get a note',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many notes',
				action: 'Get many notes',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a note',
				action: 'Update a note',
			},
		],
	},
];

export const noteDescription: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                note:create                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Memo',
		name: 'memo',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['note'],
			},
		},
	},
	// {
	// 	displayName: 'Additional Fields',
	// 	name: 'additionalFields',
	// 	type: 'collection',
	// 	default: {},
	// 	placeholder: 'Add Field',
	// 	displayOptions: {
	// 		show: {
	// 			operation: [
	// 				'create',
	// 			],
	// 			resource: [
	// 				'note',
	// 			],
	// 		},
	// 	},
	// 	options: [
	// 		{
	// 			displayName: 'Name',
	// 			name: 'name',
	// 			type: 'string',
	// 			default: '',
	// 		},
	// 	],
	// },

	/* -------------------------------------------------------------------------- */
	/*                                note:get                                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Note ID',
		name: 'noteId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get', 'delete'],
				resource: ['note'],
			},
		},
	},
	/* -------------------------------------------------------------------------- */
	/*                                note:getAll                                 */
	/* -------------------------------------------------------------------------- */

	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['note'],
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
				resource: ['note'],
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
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['getAll', 'get'],
				resource: ['note'],
			},
		},
		options: [
			{
				displayName: 'Fields to Include',
				name: 'fieldsList',
				type: 'multiOptions',
				description:
					'Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: [],
				typeOptions: {
					loadOptionsMethod: 'getModelFields',
				},
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                note:update                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Note ID',
		name: 'noteId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['note'],
			},
		},
	},
	{
		displayName: 'Memo',
		name: 'memo',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['note'],
			},
		},
	},
	// {
	// 	displayName: 'Update Fields',
	// 	name: 'updateFields',
	// 	type: 'collection',
	// 	default: {},
	// 	placeholder: 'Add Field',
	// 	displayOptions: {
	// 		show: {
	// 			operation: [
	// 				'update',
	// 			],
	// 			resource: [
	// 				'note',
	// 			],
	// 		},
	// 	},
	// 	options: [
	// 		{
	// 			displayName: 'Name',
	// 			name: 'name',
	// 			type: 'string',
	// 			default: '',
	// 		},
	// 		{
	// 			displayName: 'Memo',
	// 			name: 'memo',
	// 			type: 'string',
	// 			default: '',
	// 		},
	// 	],
	// },
];
