"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/GoToWebinar/descriptions/CoorganizerDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/GoToWebinar/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:coorganizerOperations、coorganizerFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/GoToWebinar/descriptions/CoorganizerDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/GoToWebinar/descriptions/CoorganizerDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const coorganizerOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a coorganizer',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a coorganizer',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many coorganizers',
			},
			{
				name: 'Reinvite',
				value: 'reinvite',
				action: 'Reinvite a coorganizer',
			},
		],
		displayOptions: {
			show: {
				resource: ['coorganizer'],
			},
		},
	},
];

export const coorganizerFields: INodeProperties[] = [
	// ----------------------------------
	//         coorganizer: create
	// ----------------------------------
	{
		displayName: 'Webinar Key Name or ID',
		name: 'webinarKey',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getWebinars',
		},
		required: true,
		default: [],
		description:
			'Key of the webinar that the co-organizer is hosting. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Is External',
		name: 'isExternal',
		type: 'boolean',
		required: true,
		default: false,
		description: 'Whether the co-organizer has no GoToWebinar account',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Organizer Key',
		name: 'organizerKey',
		type: 'string',
		default: '',
		description: "The co-organizer's organizer key for the webinar",
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['create'],
				isExternal: [false],
			},
		},
	},
	{
		displayName: 'Given Name',
		name: 'givenName',
		type: 'string',
		default: '',
		description: "The co-organizer's given name",
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['create'],
				isExternal: [true],
			},
		},
	},
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		description: "The co-organizer's email address",
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['create'],
				isExternal: [true],
			},
		},
	},

	// ----------------------------------
	//         coorganizer: delete
	// ----------------------------------
	{
		displayName: 'Webinar Key Name or ID',
		name: 'webinarKey',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getWebinars',
		},
		required: true,
		default: [],
		description:
			'Key of the webinar to delete. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['delete'],
			},
		},
	},
	{
		displayName: 'Co-Organizer Key',
		name: 'coorganizerKey',
		type: 'string',
		default: '',
		description: 'Key of the co-organizer to delete',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['delete'],
			},
		},
	},
	{
		displayName: 'Is External',
		name: 'isExternal',
		type: 'boolean',
		required: true,
		default: false,
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['delete'],
			},
		},
		// eslint-disable-next-line n8n-nodes-base/node-param-description-boolean-without-whether
		description:
			"By default only internal co-organizers (with a GoToWebinar account) can be deleted. If you want to use this call for external co-organizers you have to set this parameter to 'true'.",
	},

	// ----------------------------------
	//        coorganizer: getAll
	// ----------------------------------
	{
		displayName: 'Webinar Key Name or ID',
		name: 'webinarKey',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getWebinars',
		},
		required: true,
		default: [],
		description:
			'Key of the webinar to retrieve all co-organizers from. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['getAll'],
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
				resource: ['coorganizer'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 10,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------
	//      coorganizer: reinvite
	// ----------------------------------
	{
		displayName: 'Webinar Key',
		name: 'webinarKey',
		type: 'string',
		required: true,
		default: '',
		description:
			"By default only internal co-organizers (with a GoToWebinar account) can be deleted. If you want to use this call for external co-organizers you have to set this parameter to 'true'.",
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['reinvite'],
			},
		},
	},
	{
		displayName: 'Co-Organizer Key',
		name: 'coorganizerKey',
		type: 'string',
		default: '',
		description: 'Key of the co-organizer to reinvite',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['reinvite'],
			},
		},
	},
	{
		displayName: 'Is External',
		name: 'isExternal',
		type: 'boolean',
		required: true,
		default: false,
		description: 'Whether the co-organizer has no GoToWebinar account',
		displayOptions: {
			show: {
				resource: ['coorganizer'],
				operation: ['reinvite'],
			},
		},
	},
];
