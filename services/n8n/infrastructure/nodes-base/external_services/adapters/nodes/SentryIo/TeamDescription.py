"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SentryIo/TeamDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SentryIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:teamOperations、teamFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SentryIo/TeamDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SentryIo/TeamDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const teamOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['team'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new team',
				action: 'Create a team',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a team',
				action: 'Delete a team',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get team by slug',
				action: 'Get a team',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many teams',
				action: 'Get many teams',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a team',
				action: 'Update a team',
			},
		],
		default: 'get',
	},
];

export const teamFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                team:getAll                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Organization Slug Name or ID',
		name: 'organizationSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getOrganizations',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['getAll'],
			},
		},
		required: true,
		description:
			'The slug of the organization for which the teams should be listed. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['team'],
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
				resource: ['team'],
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

	/* -------------------------------------------------------------------------- */
	/*                                team:get                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Organization Slug Name or ID',
		name: 'organizationSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getOrganizations',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['get'],
			},
		},
		required: true,
		description:
			'The slug of the organization the team belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Team Slug Name or ID',
		name: 'teamSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
			loadOptionsDependsOn: ['organizationSlug'],
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['get'],
			},
		},
		required: true,
		description:
			'The slug of the team to get. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},

	/* -------------------------------------------------------------------------- */
	/*                                team:create                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Organization Slug Name or ID',
		name: 'organizationSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getOrganizations',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['create'],
			},
		},
		required: true,
		description:
			'The slug of the organization the team belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['create'],
			},
		},
		required: true,
		description: 'The name of the team',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Slug',
				name: 'slug',
				type: 'string',
				default: '',
				description:
					'The optional slug for this team. If not provided it will be auto generated from the name.',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                team:update                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Organization Slug Name or ID',
		name: 'organizationSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getOrganizations',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['update'],
			},
		},
		required: true,
		description:
			'The slug of the organization the team belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Team Slug Name or ID',
		name: 'teamSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
			loadOptionsDependsOn: ['organizationSlug'],
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['update'],
			},
		},
		required: true,
		description:
			'The slug of the team to update. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'The new name of the team',
			},
			{
				displayName: 'Slug',
				name: 'slug',
				type: 'string',
				default: '',
				description: 'The new slug of the team. Must be unique and available.',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                team:delete                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Organization Slug Name or ID',
		name: 'organizationSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getOrganizations',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['delete'],
			},
		},
		required: true,
		description:
			'The slug of the organization the team belongs to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Team Slug Name or ID',
		name: 'teamSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
			loadOptionsDependsOn: ['organizationSlug'],
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['team'],
				operation: ['delete'],
			},
		},
		required: true,
		description:
			'The slug of the team to delete. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
];
