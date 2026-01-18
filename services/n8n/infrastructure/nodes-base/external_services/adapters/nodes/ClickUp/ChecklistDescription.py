"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/ChecklistDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:checklistOperations、checklistFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/ChecklistDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/ChecklistDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const checklistOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['checklist'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a checklist',
				action: 'Create a checklist',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a checklist',
				action: 'Delete a checklist',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a checklist',
				action: 'Update a checklist',
			},
		],
		default: 'create',
	},
];

export const checklistFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                checklist:create                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Task ID',
		name: 'task',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklist'],
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
				resource: ['checklist'],
				operation: ['create'],
			},
		},
		required: true,
	},
	/* -------------------------------------------------------------------------- */
	/*                                checklist:delete                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Checklist ID',
		name: 'checklist',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklist'],
				operation: ['delete'],
			},
		},
		required: true,
	},
	/* -------------------------------------------------------------------------- */
	/*                                checklist:update                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Checklist ID',
		name: 'checklist',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['checklist'],
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
				resource: ['checklist'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Position',
				name: 'position',
				type: 'number',
				typeOptions: {
					minValue: 0,
				},
				default: 0,
			},
		],
	},
];
