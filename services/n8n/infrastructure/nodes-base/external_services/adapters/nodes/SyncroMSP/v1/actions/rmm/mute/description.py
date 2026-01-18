"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/rmm/mute/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:rmmMuteDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/rmm/mute/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/rmm/mute/description.py

import type { RmmProperties } from '../../Interfaces';

export const rmmMuteDescription: RmmProperties = [
	{
		displayName: 'RMM Alert ID',
		name: 'alertId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['rmm'],
				operation: ['mute'],
			},
		},
		default: '',
		description: 'Mute the RMM alert by ID',
	},
	{
		displayName: 'Mute Period',
		name: 'muteFor',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['rmm'],
				operation: ['mute'],
			},
		},
		// eslint-disable-next-line n8n-nodes-base/node-param-options-type-unsorted-items
		options: [
			{
				name: '1 Hour',
				value: '1-hour',
			},
			{
				name: '1 Day',
				value: '1-day',
			},
			{
				name: '2 Days',
				value: '2-days',
			},
			{
				name: '1 Week',
				value: '1-week',
			},
			{
				name: '2 Weeks',
				value: '2-weeks',
			},
			{
				name: '1 Month',
				value: '1-month',
			},
			{
				name: 'Forever',
				value: 'forever',
			},
		],
		default: '',
		description: 'Length of time to mute alert for',
	},
];
