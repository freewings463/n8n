"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Misp/descriptions/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Misp/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Misp/descriptions/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Misp/descriptions/UserDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
		noDataExpression: true,
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a user',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a user',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a user',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many users',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a user',
			},
		],
		default: 'create',
	},
];

export const userFields: INodeProperties[] = [
	// ----------------------------------------
	//               user: create
	// ----------------------------------------
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Role ID',
		name: 'role_id',
		type: 'string',
		description: 'Role IDs are available in the MISP dashboard at /roles/index',
		required: true,
		default: '',
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
				displayName: 'GPG Key',
				name: 'gpgkey',
				type: 'string',
				default: '',
			},
			{
				// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
				displayName: 'Inviter Email or ID',
				name: 'invited_by',
				type: 'options',
				default: '',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				typeOptions: {
					loadOptionsMethod: 'getUsers',
				},
			},
			{
				displayName: 'Organization Name or ID',
				name: 'org_id',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getOrgs',
				},
			},
		],
	},

	// ----------------------------------------
	//               user: delete
	// ----------------------------------------
	{
		displayName: 'User ID',
		name: 'userId',
		description: 'Numeric ID of the user',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//                user: get
	// ----------------------------------------
	{
		displayName: 'User ID',
		name: 'userId',
		description: 'Numeric ID of the user',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['user'],
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
				resource: ['user'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//               user: update
	// ----------------------------------------
	{
		displayName: 'User ID',
		name: 'userId',
		description: 'ID of the user to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['user'],
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
				resource: ['user'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
			},
			{
				displayName: 'GPG Key',
				name: 'gpgkey',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Inviter Name or ID',
				name: 'invited_by',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getUsers',
				},
			},
			{
				displayName: 'Organization Name or ID',
				name: 'org_id',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'getOrgs',
				},
			},
		],
	},
];
