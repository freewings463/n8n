"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Orbit/NoteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Orbit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:noteOperations、noteFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Orbit/NoteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Orbit/NoteDescription.py

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
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many notes for a member',
				action: 'Get many notes',
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
	/* -------------------------------------------------------------------------- */
	/*                                note:create                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Workspace Name or ID',
		name: 'workspaceId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getWorkspaces',
		},
		default: 'Deprecated',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Member ID',
		name: 'memberId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Note',
		name: 'note',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['create'],
			},
		},
	},

	/* -------------------------------------------------------------------------- */
	/*                                note:getAll                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Workspace Name or ID',
		name: 'workspaceId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getWorkspaces',
		},
		default: 'Deprecated',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Member ID',
		name: 'memberId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['note'],
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
				operation: ['getAll'],
				resource: ['note'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Resolve Member',
		name: 'resolveMember',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['note'],
			},
		},
		default: false,
	},

	/* -------------------------------------------------------------------------- */
	/*                                note:update                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Workspace Name or ID',
		name: 'workspaceId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getWorkspaces',
		},
		default: 'Deprecated',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Member ID',
		name: 'memberId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Note ID',
		name: 'noteId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Note',
		name: 'note',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['note'],
				operation: ['update'],
			},
		},
	},
];
