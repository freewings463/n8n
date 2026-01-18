"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Autopilot/ContactListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Autopilot 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactListOperations、contactListFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Autopilot/ContactListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Autopilot/ContactListDescription.py

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
				description: 'Add contact to list',
				action: 'Add a contact to a list',
			},
			{
				name: 'Exist',
				value: 'exist',
				description: 'Check if contact is on list',
				action: 'Check if a contact list exists',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many contacts from a list',
				action: 'Get many contact lists',
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
	/*                                 contactList:add                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List Name or ID',
		name: 'listId',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getLists',
		},
		type: 'options',
		displayOptions: {
			show: {
				operation: ['add', 'remove', 'exist', 'getAll'],
				resource: ['contactList'],
			},
		},
		default: '',
		description:
			'ID of the list to operate on. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Contact ID',
		name: 'contactId',
		required: true,
		type: 'string',
		displayOptions: {
			show: {
				operation: ['add', 'remove', 'exist'],
				resource: ['contactList'],
			},
		},
		default: '',
		description: 'Can be ID or email',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 contactList:getAll                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['contactList'],
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
				resource: ['contactList'],
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
];
