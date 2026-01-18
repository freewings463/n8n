"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SentryIo/ProjectDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SentryIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:projectOperations、projectFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SentryIo/ProjectDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SentryIo/ProjectDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const projectOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['project'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new project',
				action: 'Create a project',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a project',
				action: 'Delete a project',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get project by ID',
				action: 'Get a project',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many projects',
				action: 'Get many projects',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a project',
				action: 'Update a project',
			},
		],
		default: 'get',
	},
];

export const projectFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                project:create/get                          */
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
				resource: ['project'],
				operation: ['create', 'get'],
			},
		},
		required: true,
		description:
			'The slug of the organization the events belong to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Project Slug Name or ID',
		name: 'projectSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getProjects',
			loadOptionsDependsOn: ['organizationSlug'],
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['get'],
			},
		},
		required: true,
		description:
			'The slug of the project to retrieve. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
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
				resource: ['project'],
				operation: ['create'],
			},
		},
		required: true,
		description:
			'The slug of the team to create a new project for. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['create'],
			},
		},
		required: true,
		description: 'The name for the new project',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['project'],
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
					'Optionally a slug for the new project. If it’s not provided a slug is generated from the name.',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                project:getAll                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['project'],
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
				resource: ['project'],
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
	/*                                project:update                              */
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
				resource: ['project'],
				operation: ['update'],
			},
		},
		required: true,
		description:
			'The slug of the organization the project belong to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Project Slug Name or ID',
		name: 'projectSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getProjects',
			loadOptionsDependsOn: ['organizationSlug'],
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['update'],
			},
		},
		required: true,
		description:
			'The slug of the project to update. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Bookmarked',
				name: 'isBookmarked',
				type: 'boolean',
				default: false,
				// eslint-disable-next-line n8n-nodes-base/node-param-description-boolean-without-whether
				description: 'The new platform for the updated project',
			},
			{
				displayName: 'Digests Maximum Delay',
				name: 'digestsMaxDelay',
				type: 'number',
				default: 1800,
				description: 'Maximum interval to digest alerts',
			},
			{
				displayName: 'Digests Minimun Delay',
				name: 'digestsMinDelay',
				type: 'number',
				default: 60,
				description: 'Minium interval to digest alerts',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'The new name for the updated project',
			},
			{
				displayName: 'Slug',
				name: 'slug',
				type: 'string',
				default: '',
				description: 'The new slug for the updated project',
			},
			{
				displayName: 'Team',
				name: 'team',
				type: 'string',
				default: '',
				description: 'The new team name',
			},
			{
				displayName: 'Platform',
				name: 'platform',
				type: 'string',
				default: '',
				description: 'The new platform for the updated project',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                project:delete                              */
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
				resource: ['project'],
				operation: ['delete'],
			},
		},
		required: true,
		description:
			'The slug of the organization the project belong to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Project Slug Name or ID',
		name: 'projectSlug',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getProjects',
			loadOptionsDependsOn: ['organizationSlug'],
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['project'],
				operation: ['delete'],
			},
		},
		required: true,
		description:
			'The slug of the project to delete. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
];
