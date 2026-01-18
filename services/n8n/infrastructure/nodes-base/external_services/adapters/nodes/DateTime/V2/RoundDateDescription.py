"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/V2/RoundDateDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./common.descriptions。导出:RoundDateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/V2/RoundDateDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/V2/RoundDateDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { includeInputFields } from './common.descriptions';

export const RoundDateDescription: INodeProperties[] = [
	{
		displayName:
			"You can also do this using an expression, e.g. <code>{{ your_date.beginningOf('month') }}</code> or <code>{{ your_date.endOfMonth() }}</code>. <a target='_blank' href='https://docs.n8n.io/code/cookbook/luxon/'>More info</a>",
		name: 'notice',
		type: 'notice',
		default: '',
		displayOptions: {
			show: {
				operation: ['roundDate'],
			},
		},
	},
	{
		displayName: 'Date',
		name: 'date',
		type: 'string',
		description: 'The date that you want to round',
		default: '',
		displayOptions: {
			show: {
				operation: ['roundDate'],
			},
		},
	},
	{
		displayName: 'Mode',
		name: 'mode',
		type: 'options',
		options: [
			{
				name: 'Round Down',
				value: 'roundDown',
			},
			{
				name: 'Round Up',
				value: 'roundUp',
			},
		],
		default: 'roundDown',
		displayOptions: {
			show: {
				operation: ['roundDate'],
			},
		},
	},
	{
		displayName: 'To Nearest',
		name: 'toNearest',
		type: 'options',
		// eslint-disable-next-line n8n-nodes-base/node-param-options-type-unsorted-items
		options: [
			{
				name: 'Year',
				value: 'year',
			},
			{
				name: 'Month',
				value: 'month',
			},
			{
				name: 'Week',
				value: 'week',
			},
			{
				name: 'Day',
				value: 'day',
			},
			{
				name: 'Hour',
				value: 'hour',
			},
			{
				name: 'Minute',
				value: 'minute',
			},
			{
				name: 'Second',
				value: 'second',
			},
		],
		default: 'month',
		displayOptions: {
			show: {
				operation: ['roundDate'],
				mode: ['roundDown'],
			},
		},
	},
	{
		displayName: 'To',
		name: 'to',
		type: 'options',
		options: [
			{
				name: 'End of Month',
				value: 'month',
			},
		],
		default: 'month',
		displayOptions: {
			show: {
				operation: ['roundDate'],
				mode: ['roundUp'],
			},
		},
	},
	{
		displayName: 'Output Field Name',
		name: 'outputFieldName',
		type: 'string',
		default: 'roundedDate',
		description: 'Name of the field to put the output in',
		displayOptions: {
			show: {
				operation: ['roundDate'],
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
				operation: ['roundDate'],
			},
		},
		default: {},
		options: [includeInputFields],
	},
];
