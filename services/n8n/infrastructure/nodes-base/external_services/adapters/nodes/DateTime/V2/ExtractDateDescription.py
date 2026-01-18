"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/V2/ExtractDateDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./common.descriptions。导出:ExtractDateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/V2/ExtractDateDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/V2/ExtractDateDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { includeInputFields } from './common.descriptions';

export const ExtractDateDescription: INodeProperties[] = [
	{
		displayName:
			'You can also do this using an expression, e.g. <code>{{ your_date.extract("month") }}}</code>. <a target="_blank" href="https://docs.n8n.io/code/cookbook/luxon/">More info</a>',
		name: 'notice',
		type: 'notice',
		default: '',
		displayOptions: {
			show: {
				operation: ['extractDate'],
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
				operation: ['extractDate'],
			},
		},
	},
	{
		displayName: 'Part',
		name: 'part',
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
				operation: ['extractDate'],
			},
		},
	},
	{
		displayName: 'Output Field Name',
		name: 'outputFieldName',
		type: 'string',
		default: 'datePart',
		description: 'Name of the field to put the output in',
		displayOptions: {
			show: {
				operation: ['extractDate'],
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
				operation: ['extractDate'],
			},
		},
		default: {},
		options: [includeInputFields],
	},
];
