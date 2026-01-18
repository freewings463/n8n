"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Demio/ReportDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Demio 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:reportOperations、reportFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Demio/ReportDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Demio/ReportDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const reportOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['report'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get an event report',
				action: 'Get a report',
			},
		],
		default: 'get',
	},
];

export const reportFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   report:get                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Event Name or ID',
		name: 'eventId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getEvents',
		},
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['get'],
			},
		},
		default: '',
	},
	{
		displayName: 'Session Name or ID',
		name: 'dateId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getEventSessions',
			loadOptionsDependsOn: ['eventId'],
		},
		default: '',
		required: true,
		description:
			'ID of the session. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['get'],
			},
		},
		options: [
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				options: [
					{
						name: 'Attended',
						value: 'attended',
					},
					{
						name: 'Banned',
						value: 'banned',
					},
					{
						name: 'Completed',
						value: 'completed',
					},
					{
						name: 'Did Not Attend',
						value: 'did-not-attend',
					},
					{
						name: 'Left Early',
						value: 'left-early',
					},
				],
				default: '',
				description: 'Filter results by participation status',
			},
		],
	},
];
