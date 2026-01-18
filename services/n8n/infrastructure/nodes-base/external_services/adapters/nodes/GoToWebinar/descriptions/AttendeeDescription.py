"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/GoToWebinar/descriptions/AttendeeDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/GoToWebinar/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:attendeeOperations、attendeeFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/GoToWebinar/descriptions/AttendeeDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/GoToWebinar/descriptions/AttendeeDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const attendeeOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get an attendee',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many attendees',
			},
			{
				name: 'Get Details',
				value: 'getDetails',
				action: 'Get details of an attendee',
			},
		],
		displayOptions: {
			show: {
				resource: ['attendee'],
			},
		},
	},
];

export const attendeeFields: INodeProperties[] = [
	// ----------------------------------
	//     attendee: shared fields
	// ----------------------------------
	{
		displayName: 'Webinar Key Name or ID',
		name: 'webinarKey',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getWebinars',
		},
		required: true,
		default: '',
		description:
			'Key of the webinar that the attendee attended. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['attendee'],
			},
		},
	},
	{
		displayName: 'Session Key Name or ID',
		name: 'sessionKey',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getWebinarSessions',
			loadOptionsDependsOn: ['webinarKey'],
		},
		default: '',
		description:
			'Key of the session that the attendee attended. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['attendee'],
			},
		},
	},

	// ----------------------------------
	//          attendee: get
	// ----------------------------------
	{
		displayName: 'Registrant Key',
		name: 'registrantKey',
		type: 'string',
		required: true,
		default: '',
		description: 'Registrant key of the attendee at the webinar session',
		displayOptions: {
			show: {
				resource: ['attendee'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//       attendee: getDetails
	// ----------------------------------
	{
		displayName: 'Registrant Key',
		name: 'registrantKey',
		type: 'string',
		required: true,
		default: '',
		description: 'Registrant key of the attendee at the webinar session',
		displayOptions: {
			show: {
				resource: ['attendee'],
				operation: ['getDetails'],
			},
		},
	},
	{
		displayName: 'Details',
		name: 'details',
		type: 'options',
		required: true,
		default: '',
		description: 'The details to retrieve for the attendee',
		options: [
			{
				name: 'Polls',
				value: 'polls',
				description: 'Poll answers from the attendee in a webinar session',
			},
			{
				name: 'Questions',
				value: 'questions',
				description: 'Questions asked by the attendee in a webinar session',
			},
			{
				name: 'Survey Answers',
				value: 'surveyAnswers',
				description: 'Survey answers from the attendee in a webinar session',
			},
		],
		displayOptions: {
			show: {
				resource: ['attendee'],
				operation: ['getDetails'],
			},
		},
	},

	// ----------------------------------
	//         attendee: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['attendee'],
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
				resource: ['attendee'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
];
