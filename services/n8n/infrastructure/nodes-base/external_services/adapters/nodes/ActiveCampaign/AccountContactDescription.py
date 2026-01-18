"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActiveCampaign/AccountContactDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActiveCampaign 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:accountContactOperations、accountContactFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActiveCampaign/AccountContactDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActiveCampaign/AccountContactDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const accountContactOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['accountContact'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an association',
				action: 'Create an account contact',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an association',
				action: 'Delete an account contact',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an association',
				action: 'Update an account contact',
			},
		],
		default: 'create',
	},
];

export const accountContactFields: INodeProperties[] = [
	// ----------------------------------
	//         accountContact:create
	// ----------------------------------
	{
		displayName: 'Account ID',
		name: 'account',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['accountContact'],
			},
		},
	},
	{
		displayName: 'Contact ID',
		name: 'contact',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['accountContact'],
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
				operation: ['create'],
				resource: ['accountContact'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Job Title',
				name: 'jobTitle',
				type: 'string',
				default: '',
				description: 'Job Title of the contact at the account',
			},
		],
	},
	// ----------------------------------
	//         accountContact:delete
	// ----------------------------------
	{
		displayName: 'Account Contact ID',
		name: 'accountContactId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['accountContact'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the account contact to delete',
	},
	// ----------------------------------
	//         accountContact:update
	// ----------------------------------
	{
		displayName: 'Account Contact ID',
		name: 'accountContactId',
		type: 'number',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['accountContact'],
			},
		},
		description: 'Account ID',
	},

	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		description: 'The fields to update',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['accountContact'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Job Title',
				name: 'jobTitle',
				type: 'string',
				default: '',
				description: 'Job Title of the contact at the account',
			},
		],
	},
];
