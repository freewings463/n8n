"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cisco/Webex/descriptions/MeetingTranscript.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cisco/Webex 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:meetingTranscriptOperations、meetingTranscriptFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cisco/Webex/descriptions/MeetingTranscript.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cisco/Webex/descriptions/MeetingTranscript.py

import type { INodeProperties } from 'n8n-workflow';

export const meetingTranscriptOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
			},
		},
		options: [
			{
				name: 'Download',
				value: 'download',
				action: 'Download a meeting transcript',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many meeting transcripts',
			},
		],
		default: 'download',
	},
];

export const meetingTranscriptFields: INodeProperties[] = [
	// ----------------------------------------
	//             meetingTranscript: download
	// ----------------------------------------
	{
		displayName: 'Transcript ID',
		name: 'transcriptId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
				operation: ['download'],
			},
		},
		description: 'Unique identifier for the meeting transcript',
	},
	{
		displayName: 'Meeting ID',
		name: 'meetingId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
				operation: ['download'],
			},
		},
		description: 'Unique identifier for the meeting instance which the transcripts belong to',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
				operation: ['download'],
			},
		},
		default: {},
		placeholder: 'Add option',
		options: [
			{
				displayName: 'Format',
				name: 'format',
				type: 'options',
				options: [
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
						name: 'txt',
						value: 'txt',
					},
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
						name: 'vtt',
						value: 'vtt',
					},
				],
				default: 'vtt',
				description: 'Format for the downloaded meeting transcript',
			},
		],
	},

	// ----------------------------------------
	//             meetingTranscript: getAll
	// ----------------------------------------
	{
		displayName: 'Meeting ID',
		name: 'meetingId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
				operation: ['getAll'],
			},
		},
		description: 'Unique identifier for the meeting instance which the transcripts belong to',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
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
				resource: ['meetingTranscript'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['meetingTranscript'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Host Email',
				name: 'hostEmail',
				type: 'string',
				default: '',
				description: 'Email address for the meetingTranscript host',
			},
		],
	},
];
