"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/FreshworksCrm/descriptions/NoteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/FreshworksCrm/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:noteOperations、noteFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/FreshworksCrm/descriptions/NoteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/FreshworksCrm/descriptions/NoteDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const noteOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
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
				description: 'Create a note',
				action: 'Create a note',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a note',
				action: 'Delete a note',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a note',
				action: 'Update a note',
			},
		],
		default: 'create',
	},
];

export const noteFields: INodeProperties[] = [
	// ----------------------------------------
	//               note: create
	// ----------------------------------------
	{
		displayName: 'Content',
		name: 'description',
		description: 'Content of the note',
		type: 'string',
		required: true,
		typeOptions: {
			rows: 5,
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Target Type',
		name: 'targetableType',
		description: 'Type of the entity for which the note is created',
		type: 'options',
		required: true,
		default: 'Contact',
		options: [
			{
				name: 'Contact',
				value: 'Contact',
			},
			{
				name: 'Deal',
				value: 'Deal',
			},
			{
				name: 'Sales Account',
				value: 'SalesAccount',
			},
		],
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Target ID',
		name: 'targetable_id',
		description:
			'ID of the entity for which note is created. The type of entity is selected in "Target Type".',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['create'],
			},
		},
	},

	// ----------------------------------------
	//               note: delete
	// ----------------------------------------
	{
		displayName: 'Note ID',
		name: 'noteId',
		description: 'ID of the note to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//               note: update
	// ----------------------------------------
	{
		displayName: 'Note ID',
		name: 'noteId',
		description: 'ID of the note to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['note'],
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
				resource: ['note'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Content',
				name: 'description',
				type: 'string',
				typeOptions: {
					rows: 5,
				},
				default: '',
				description: 'Content of the note',
			},
			{
				displayName: 'Target ID',
				name: 'targetable_id',
				type: 'string',
				default: '',
				description: 'ID of the entity for which the note is updated',
			},
			{
				displayName: 'Target Type',
				name: 'targetable_type',
				type: 'options',
				default: 'Contact',
				description: 'Type of the entity for which the note is updated',
				options: [
					{
						name: 'Contact',
						value: 'Contact',
					},
					{
						name: 'Deal',
						value: 'Deal',
					},
					{
						name: 'Sales Account',
						value: 'SalesAccount',
					},
				],
			},
		],
	},
];
