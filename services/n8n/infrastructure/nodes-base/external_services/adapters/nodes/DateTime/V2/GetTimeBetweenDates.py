"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/V2/GetTimeBetweenDates.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./common.descriptions。导出:GetTimeBetweenDatesDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/V2/GetTimeBetweenDates.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/V2/GetTimeBetweenDates.py

import type { INodeProperties } from 'n8n-workflow';

import { includeInputFields } from './common.descriptions';

export const GetTimeBetweenDatesDescription: INodeProperties[] = [
	{
		displayName: 'Start Date',
		name: 'startDate',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				operation: ['getTimeBetweenDates'],
			},
		},
	},
	{
		displayName: 'End Date',
		name: 'endDate',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				operation: ['getTimeBetweenDates'],
			},
		},
	},
	{
		displayName: 'Units',
		name: 'units',
		type: 'multiOptions',
		// eslint-disable-next-line n8n-nodes-base/node-param-multi-options-type-unsorted-items
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
			{
				name: 'Millisecond',
				value: 'millisecond',
			},
		],
		displayOptions: {
			show: {
				operation: ['getTimeBetweenDates'],
			},
		},
		default: ['day'],
	},
	{
		displayName: 'Output Field Name',
		name: 'outputFieldName',
		type: 'string',
		default: 'timeDifference',
		description: 'Name of the field to put the output in',
		displayOptions: {
			show: {
				operation: ['getTimeBetweenDates'],
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
				operation: ['getTimeBetweenDates'],
			},
		},
		default: {},
		options: [
			includeInputFields,
			{
				displayName: 'Output as ISO String',
				name: 'isoString',
				type: 'boolean',
				default: false,
				description: 'Whether to output the date as ISO string or not',
			},
		],
	},
];
