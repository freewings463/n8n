"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MonicaCrm/descriptions/JournalEntryDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MonicaCrm/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:journalEntryOperations、journalEntryFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MonicaCrm/descriptions/JournalEntryDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MonicaCrm/descriptions/JournalEntryDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const journalEntryOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['journalEntry'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a journal entry',
				action: 'Create a journal entry',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a journal entry',
				action: 'Delete a journal entry',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a journal entry',
				action: 'Get a journal entry',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many journal entries',
				action: 'Get many journal entries',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a journal entry',
				action: 'Update a journal entry',
			},
		],
		default: 'create',
	},
];

export const journalEntryFields: INodeProperties[] = [
	// ----------------------------------------
	//           journalEntry: create
	// ----------------------------------------
	{
		displayName: 'Title',
		name: 'title',
		description: 'Title of the journal entry - max 250 characters',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['journalEntry'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Content',
		name: 'post',
		description: 'Content of the journal entry - max 100,000 characters',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['journalEntry'],
				operation: ['create'],
			},
		},
	},

	// ----------------------------------------
	//           journalEntry: delete
	// ----------------------------------------
	{
		displayName: 'Journal Entry ID',
		name: 'journalId',
		description: 'ID of the journal entry to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['journalEntry'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//            journalEntry: get
	// ----------------------------------------
	{
		displayName: 'Journal Entry ID',
		name: 'journalId',
		description: 'ID of the journal entry to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['journalEntry'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//           journalEntry: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['journalEntry'],
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
				resource: ['journalEntry'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//           journalEntry: update
	// ----------------------------------------
	{
		displayName: 'Journal Entry ID',
		name: 'journalId',
		description: 'ID of the journal entry to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['journalEntry'],
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
				resource: ['journalEntry'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Content',
				name: 'post',
				description: 'Content of the journal entry - max 100,000 characters',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Title',
				name: 'title',
				description: 'Title of the journal entry - max 250 characters',
				type: 'string',
				default: '',
			},
		],
	},
];
