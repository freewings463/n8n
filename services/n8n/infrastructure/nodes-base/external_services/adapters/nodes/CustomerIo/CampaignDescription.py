"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/CustomerIo/CampaignDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/CustomerIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:campaignOperations、campaignFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/CustomerIo/CampaignDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/CustomerIo/CampaignDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const campaignOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['campaign'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get a campaign',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many campaigns',
			},
			{
				name: 'Get Metrics',
				value: 'getMetrics',
				action: 'Get metrics for a campaign',
			},
		],
		default: 'get',
	},
];

export const campaignFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   campaign:get                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Campaign ID',
		name: 'campaignId',
		type: 'number',
		required: true,
		default: 0,
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['get'],
			},
		},
		description: 'The unique identifier for the campaign',
	},
	/* -------------------------------------------------------------------------- */
	/*                                   campaign:getMetrics                      */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Campaign ID',
		name: 'campaignId',
		type: 'number',
		required: true,
		default: 0,
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getMetrics'],
			},
		},
		description: 'The unique identifier for the campaign',
	},
	{
		displayName: 'Period',
		name: 'period',
		type: 'options',
		default: 'days',
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getMetrics'],
			},
		},
		description: 'Specify metric period',
		options: [
			{
				name: 'Hours',
				value: 'hours',
			},
			{
				name: 'Days',
				value: 'days',
			},
			{
				name: 'Weeks',
				value: 'weeks',
			},
			{
				name: 'Months',
				value: 'months',
			},
		],
	},
	{
		displayName: 'JSON Parameters',
		name: 'jsonParameters',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['campaign'],
				operation: ['getMetrics'],
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
				resource: ['campaign'],
				operation: ['getMetrics'],
				jsonParameters: [false],
			},
		},
		options: [
			{
				displayName: 'Steps',
				name: 'steps',
				type: 'number',
				default: 0,
				description:
					'Integer specifying how many steps to return. Defaults to the maximum number of timeperiods available, or 12 when using the months period. Maximum timeperiods available are 24 hours, 45 days, 12 weeks and 120 months',
				typeOptions: {
					minValue: 0,
					maxValue: 120,
				},
			},
			{
				displayName: 'Type',
				name: 'type',
				type: 'options',
				default: 'empty',
				description: 'Specify metric type',
				options: [
					{
						name: 'Email',
						value: 'email',
					},
					{
						name: 'Empty',
						value: 'empty',
					},
					{
						name: 'Push',
						value: 'push',
					},
					{
						name: 'Slack',
						value: 'slack',
					},
					{
						name: 'Twilio',
						value: 'twilio',
					},
					{
						name: 'Urban Airship',
						value: 'urbanAirship',
					},
					{
						name: 'Webhook',
						value: 'webhook',
					},
				],
			},
		],
	},
];
