"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/GoToWebinar/descriptions/PanelistDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/GoToWebinar/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:panelistOperations、panelistFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/GoToWebinar/descriptions/PanelistDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/GoToWebinar/descriptions/PanelistDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const panelistOperations: INodeProperties[] = [
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
				action: 'Create a panelist',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a panelist',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many panelists',
			},
			{
				name: 'Reinvite',
				value: 'reinvite',
				action: 'Reinvite a panelist',
			},
		],
		displayOptions: {
			show: {
				resource: ['panelist'],
			},
		},
	},
];

export const panelistFields: INodeProperties[] = [
	// ----------------------------------
	//        panelist: create
	// ----------------------------------
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		description: 'Name of the panelist to create',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		required: true,
		default: '',
		description: 'Email address of the panelist to create',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['create'],
			},
		},
	},
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
			'Key of the webinar that the panelist will present at. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['create'],
			},
		},
	},

	// ----------------------------------
	//        panelist: getAll
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
			'Key of the webinar to retrieve all panelists from. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['panelist'],
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
				resource: ['panelist'],
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
				resource: ['panelist'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------
	//        panelist: delete
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
			'Key of the webinar to delete the panelist from. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['delete'],
			},
		},
	},
	{
		displayName: 'Panelist Key',
		name: 'panelistKey',
		type: 'string',
		required: true,
		default: '',
		description: 'Key of the panelist to delete',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------
	//        panelist: reinvite
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
			'Key of the webinar to reinvite the panelist to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['reinvite'],
			},
		},
	},
	{
		displayName: 'Panelist Key',
		name: 'panelistKey',
		type: 'string',
		required: true,
		default: '',
		description: 'Key of the panelist to reinvite',
		displayOptions: {
			show: {
				resource: ['panelist'],
				operation: ['reinvite'],
			},
		},
	},
];
