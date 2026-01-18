"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/V2/CurrentDateDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./common.descriptions。导出:CurrentDateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/V2/CurrentDateDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/V2/CurrentDateDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { includeInputFields } from './common.descriptions';

export const CurrentDateDescription: INodeProperties[] = [
	{
		displayName:
			'You can also refer to the current date in n8n expressions by using <code>{{$now}}</code> or <code>{{$today}}</code>. <a target="_blank" href="https://docs.n8n.io/code/cookbook/luxon/">More info</a>',
		name: 'notice',
		type: 'notice',
		default: '',
		displayOptions: {
			show: {
				operation: ['getCurrentDate'],
			},
		},
	},
	{
		displayName: 'Include Current Time',
		name: 'includeTime',
		type: 'boolean',
		default: true,
		// eslint-disable-next-line n8n-nodes-base/node-param-description-boolean-without-whether
		description: 'When deactivated, the time will be set to midnight',
		displayOptions: {
			show: {
				operation: ['getCurrentDate'],
			},
		},
	},
	{
		displayName: 'Output Field Name',
		name: 'outputFieldName',
		type: 'string',
		default: 'currentDate',
		description: 'Name of the field to put the output in',
		displayOptions: {
			show: {
				operation: ['getCurrentDate'],
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
				operation: ['getCurrentDate'],
			},
		},
		default: {},
		options: [
			includeInputFields,
			{
				displayName: 'Timezone',
				name: 'timezone',
				type: 'string',
				placeholder: 'America/New_York',
				default: '',
				description:
					'The timezone to use. If not set, the timezone of the n8n instance will be used. Use ‘GMT’ for +00:00 timezone.',
			},
		],
	},
];
