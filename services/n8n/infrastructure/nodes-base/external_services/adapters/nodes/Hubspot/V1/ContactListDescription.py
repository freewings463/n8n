"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Hubspot/V1/ContactListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Hubspot/V1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactListOperations、contactListFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Hubspot/V1/ContactListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Hubspot/V1/ContactListDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const contactListOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add contact to a list',
				action: 'Add a contact to a list',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a contact from a list',
				action: 'Remove a contact from a list',
			},
		],
		default: 'add',
	},
];

export const contactListFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                contactList:add                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'By',
		name: 'by',
		type: 'options',
		options: [
			{
				name: 'Contact ID',
				value: 'id',
			},
			{
				name: 'Email',
				value: 'email',
			},
		],
		required: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
				operation: ['add'],
			},
		},
		default: 'email',
	},
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
				operation: ['add'],
				by: ['email'],
			},
		},
		default: '',
	},
	{
		displayName: 'Contact ID',
		name: 'id',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
				operation: ['add'],
				by: ['id'],
			},
		},
		default: '',
	},
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
				operation: ['add'],
			},
		},
		default: '',
	},

	/* -------------------------------------------------------------------------- */
	/*                                contactList:remove                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Contact ID',
		name: 'id',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
				operation: ['remove'],
			},
		},
		default: '',
	},
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactList'],
				operation: ['remove'],
			},
		},
		default: '',
	},
];
