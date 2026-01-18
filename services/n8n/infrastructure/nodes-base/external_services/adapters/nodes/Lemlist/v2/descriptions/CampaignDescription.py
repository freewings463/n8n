"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Lemlist/v2/descriptions/CampaignDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Lemlist/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:campaignOperations、campaignFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Lemlist/v2/descriptions/CampaignDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Lemlist/v2/descriptions/CampaignDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const campaignOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'getAll',
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many campaigns',
			},
			{
				name: 'Get Stats',
				value: 'getStats',
				action: 'Get campaign stats',
			},
		],
		displayOptions: {
			show: {
				resource: ['campaign'],
			},
		},
	},
];

export const campaignFields: INodeProperties[] = [
	// ----------------------------------
	//        campaign: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 5,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		displayOptions: {
			show: {
				resource: ['campaign'],
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
				resource: ['campaign'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Version',
				name: 'version',
				type: 'string',
				default: 'v2',
			},
		],
	},
	// ----------------------------------
	//        campaign: getStats
	// ----------------------------------
	{
		displayName: 'Campaign Name or ID',
		name: 'campaignId',
		type: 'options',
		required: true,
		default: [],
		typeOptions: {
			loadOptionsMethod: 'getCampaigns',
		},
		description:
			'ID of the campaign to get stats for. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getStats'],
			},
		},
	},
	{
		displayName: 'Start Date',
		name: 'startDate',
		type: 'dateTime',
		default: '',
		required: true,
		placeholder: 'e.g. 2024-09-03 00:00:00Z',
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getStats'],
			},
		},
	},
	{
		displayName: 'End Date',
		name: 'endDate',
		type: 'dateTime',
		default: '',
		placeholder: 'e.g. 2024-09-03 00:00:00Z',
		required: true,
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getStats'],
			},
		},
	},
	{
		displayName: 'Timezone',
		name: 'timezone',
		type: 'string',
		default: '',
		required: true,
		placeholder: 'e.g. Europe/Paris',
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getStats'],
			},
		},
	},
];
