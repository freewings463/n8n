"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/ChecklistItemDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:checklistItemOperations、checklistItemFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/ChecklistItemDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/ChecklistItemDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const checklistItemOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['checklistItem'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a checklist item',
				action: 'Create a checklist item',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a checklist item',
				action: 'Delete a checklist item',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a checklist item',
				action: 'Update a checklist item',
			},
		],
		default: 'create',
	},
];

export const checklistItemFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                checklistItem:create                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Checklist ID',
		name: 'checklist',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklistItem'],
				operation: ['create'],
			},
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
				resource: ['checklistItem'],
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
				resource: ['checklistItem'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Assignee ID',
				name: 'assignee',
				type: 'string',
				default: '',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                checklistItem:delete                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Checklist ID',
		name: 'checklist',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklistItem'],
				operation: ['delete'],
			},
		},
		required: true,
	},
	{
		displayName: 'Checklist Item ID',
		name: 'checklistItem',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklistItem'],
				operation: ['delete'],
			},
		},
		required: true,
	},

	/* -------------------------------------------------------------------------- */
	/*                                checklistItem:update                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Checklist ID',
		name: 'checklist',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklistItem'],
				operation: ['update'],
			},
		},
		required: true,
	},
	{
		displayName: 'Checklist Item ID',
		name: 'checklistItem',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklistItem'],
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
				resource: ['checklistItem'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Assignee ID',
				name: 'assignee',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Parent Checklist Item ID',
				name: 'parent',
				type: 'string',
				default: '',
				description: 'Checklist item that you want to nest the target checklist item underneath',
			},
			{
				displayName: 'Resolved',
				name: 'resolved',
				type: 'boolean',
				default: false,
			},
		],
	},
];
