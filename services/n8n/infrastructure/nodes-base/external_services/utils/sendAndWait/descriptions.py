"""
MIGRATION-META:
  source_path: packages/nodes-base/utils/sendAndWait/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/utils/sendAndWait 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:sendAndWaitWebhooksDescription、limitWaitTimeProperties。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/utils/sendAndWait/descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/utils/sendAndWait/descriptions.py

import type { INodeProperties, IWebhookDescription } from 'n8n-workflow';

export const sendAndWaitWebhooksDescription: IWebhookDescription[] = [
	{
		name: 'default',
		httpMethod: 'GET',
		responseMode: 'onReceived',
		responseData: '',
		path: '={{ $nodeId }}',
		restartWebhook: true,
		isFullPath: true,
	},
	{
		name: 'default',
		httpMethod: 'POST',
		responseMode: 'onReceived',
		responseData: '',
		path: '={{ $nodeId }}',
		restartWebhook: true,
		isFullPath: true,
	},
];

export const limitWaitTimeProperties: INodeProperties[] = [
	{
		displayName: 'Limit Type',
		name: 'limitType',
		type: 'options',
		default: 'afterTimeInterval',
		description:
			'Sets the condition for the execution to resume. Can be a specified date or after some time.',
		options: [
			{
				name: 'After Time Interval',
				description: 'Waits for a certain amount of time',
				value: 'afterTimeInterval',
			},
			{
				name: 'At Specified Time',
				description: 'Waits until the set date and time to continue',
				value: 'atSpecifiedTime',
			},
		],
	},
	{
		displayName: 'Amount',
		name: 'resumeAmount',
		type: 'number',
		displayOptions: {
			show: {
				limitType: ['afterTimeInterval'],
			},
		},
		typeOptions: {
			minValue: 0,
			numberPrecision: 2,
		},
		default: 1,
		description: 'The time to wait',
	},
	{
		displayName: 'Unit',
		name: 'resumeUnit',
		type: 'options',
		displayOptions: {
			show: {
				limitType: ['afterTimeInterval'],
			},
		},
		options: [
			{
				name: 'Minutes',
				value: 'minutes',
			},
			{
				name: 'Hours',
				value: 'hours',
			},
			{
				name: 'Days',
				value: 'days',
			},
		],
		default: 'hours',
		description: 'Unit of the interval value',
	},
	{
		displayName: 'Max Date and Time',
		name: 'maxDateAndTime',
		type: 'dateTime',
		displayOptions: {
			show: {
				limitType: ['atSpecifiedTime'],
			},
		},
		default: '',
		description: 'Continue execution after the specified date and time',
	},
];
