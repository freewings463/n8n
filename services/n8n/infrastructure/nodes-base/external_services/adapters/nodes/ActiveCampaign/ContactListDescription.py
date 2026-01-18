"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActiveCampaign/ContactListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActiveCampaign 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactListOperations、contactListFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActiveCampaign/ContactListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActiveCampaign/ContactListDescription.py

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
				description: 'Remove contact from a list',
				action: 'Remove a contact from a list',
			},
		],
		default: 'add',
	},
];

export const contactListFields: INodeProperties[] = [
	// ----------------------------------
	//         contactList:add
	// ----------------------------------
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['add'],
				resource: ['contactList'],
			},
		},
	},
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['add'],
				resource: ['contactList'],
			},
		},
	},

	// ----------------------------------
	//         contactList:remove
	// ----------------------------------
	{
		displayName: 'List ID',
		name: 'listId',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['remove'],
				resource: ['contactList'],
			},
		},
	},
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['remove'],
				resource: ['contactList'],
			},
		},
	},
];
