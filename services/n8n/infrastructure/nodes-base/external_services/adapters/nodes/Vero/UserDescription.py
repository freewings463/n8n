"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Vero/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Vero 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Vero/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Vero/UserDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
		options: [
			{
				name: 'Add Tags',
				value: 'addTags',
				description: 'Adds a tag to a users profile',
				action: 'Add tags to a user',
			},
			{
				name: 'Alias',
				value: 'alias',
				description: 'Change a users identifier',
				action: "Change a user's alias",
			},
			{
				name: 'Create or Update',
				value: 'create',
				description: 'Create or update a user profile',
				action: 'Create or update a user',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a user',
				action: 'Delete a user',
			},
			{
				name: 'Re-Subscribe',
				value: 'resubscribe',
				description: 'Resubscribe a user',
				action: 'Resubscribe a user',
			},
			{
				name: 'Remove Tags',
				value: 'removeTags',
				description: 'Removes a tag from a users profile',
				action: 'Remove tags from a user',
			},
			{
				name: 'Unsubscribe',
				value: 'unsubscribe',
				description: 'Unsubscribe a user',
				action: 'Unsubscribe a user',
			},
		],
		default: 'create',
	},
];

export const userFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                user:create                                 */
	/* -------------------------------------------------------------------------- */

	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		description: 'The unique identifier of the customer',
	},
	{
		displayName: 'JSON Parameters',
		name: 'jsonParameters',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
				description: 'The table to create the row in',
			},
		],
	},
	{
		displayName: 'Data',
		name: 'dataAttributesUi',
		placeholder: 'Add Data',
		description: 'Key value pairs that represent the custom user properties you want to update',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
				jsonParameters: [false],
			},
		},
		options: [
			{
				name: 'dataAttributesValues',
				displayName: 'Data',
				values: [
					{
						displayName: 'Key',
						name: 'key',
						type: 'string',
						default: '',
						description: 'Name of the property to set',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the property to set',
					},
				],
			},
		],
	},
	{
		displayName: 'Data',
		name: 'dataAttributesJson',
		type: 'json',
		default: '',
		typeOptions: {
			alwaysOpenEditWindow: true,
		},
		description: 'Key value pairs that represent the custom user properties you want to update',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
				jsonParameters: [true],
			},
		},
	},

	/* -------------------------------------------------------------------------- */
	/*                                   user:alias                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['alias'],
			},
		},
		description: 'The old unique identifier of the user',
	},
	{
		displayName: 'New ID',
		name: 'newId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['alias'],
			},
		},
		description: 'The new unique identifier of the user',
	},
	/* -------------------------------------------------------------------------- */
	/*                                   user:unsubscribe                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['unsubscribe'],
			},
		},
		description: 'The unique identifier of the user',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 user:resubscribe                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['resubscribe'],
			},
		},
		description: 'The unique identifier of the user',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 user:delete                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['delete'],
			},
		},
		description: 'The unique identifier of the user',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 user:addTags                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['addTags'],
			},
		},
		description: 'The unique identifier of the user',
	},
	{
		displayName: 'Tags',
		name: 'tags',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['addTags'],
			},
		},
		description: 'Tags to add separated by ","',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 user:removeTags                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'ID',
		name: 'id',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['removeTags'],
			},
		},
		description: 'The unique identifier of the user',
	},
	{
		displayName: 'Tags',
		name: 'tags',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['removeTags'],
			},
		},
		description: 'Tags to remove separated by ","',
	},
];
