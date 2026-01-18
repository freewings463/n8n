"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/V2/SubtractFromDateDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./common.descriptions。导出:SubtractFromDateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/V2/SubtractFromDateDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/V2/SubtractFromDateDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { includeInputFields } from './common.descriptions';

export const SubtractFromDateDescription: INodeProperties[] = [
	{
		displayName:
			"You can also do this using an expression, e.g. <code>{{your_date.minus(5, 'minutes')}}</code>. <a target='_blank' href='https://docs.n8n.io/code/cookbook/luxon/'>More info</a>",
		name: 'notice',
		type: 'notice',
		default: '',
		displayOptions: {
			show: {
				operation: ['subtractFromDate'],
			},
		},
	},
	{
		displayName: 'Date to Subtract From',
		name: 'magnitude',
		type: 'string',
		description: 'The date that you want to change',
		default: '',
		displayOptions: {
			show: {
				operation: ['subtractFromDate'],
			},
		},
		required: true,
	},
	{
		displayName: 'Time Unit to Subtract',
		name: 'timeUnit',
		description: 'Time unit for Duration parameter below',
		displayOptions: {
			show: {
				operation: ['subtractFromDate'],
			},
		},
		type: 'options',
		// eslint-disable-next-line n8n-nodes-base/node-param-options-type-unsorted-items
		options: [
			{
				name: 'Years',
				value: 'years',
			},
			{
				name: 'Quarters',
				value: 'quarters',
			},
			{
				name: 'Months',
				value: 'months',
			},
			{
				name: 'Weeks',
				value: 'weeks',
			},
			{
				name: 'Days',
				value: 'days',
			},
			{
				name: 'Hours',
				value: 'hours',
			},
			{
				name: 'Minutes',
				value: 'minutes',
			},
			{
				name: 'Seconds',
				value: 'seconds',
			},
			{
				name: 'Milliseconds',
				value: 'milliseconds',
			},
		],
		default: 'days',
		required: true,
	},
	{
		displayName: 'Duration',
		name: 'duration',
		type: 'number',
		description: 'The number of time units to subtract from the date',
		default: 0,
		displayOptions: {
			show: {
				operation: ['subtractFromDate'],
			},
		},
	},
	{
		displayName: 'Output Field Name',
		name: 'outputFieldName',
		type: 'string',
		default: 'newDate',
		description: 'Name of the field to put the output in',
		displayOptions: {
			show: {
				operation: ['subtractFromDate'],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		displayOptions: {
			show: {
				operation: ['subtractFromDate'],
			},
		},
		default: {},
		options: [includeInputFields],
	},
];
