"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/CustomerIo/SegmentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/CustomerIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:segmentOperations、segmentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/CustomerIo/SegmentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/CustomerIo/SegmentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const segmentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['segment'],
			},
		},
		options: [
			{
				name: 'Add Customer',
				value: 'add',
				action: 'Add a customer to a segment',
			},
			{
				name: 'Remove Customer',
				value: 'remove',
				action: 'Remove a customer from a segment',
			},
		],
		default: 'add',
	},
];

export const segmentFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   segment:add                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Segment ID',
		name: 'segmentId',
		type: 'number',
		required: true,
		default: 0,
		displayOptions: {
			show: {
				resource: ['segment'],
				operation: ['add', 'remove'],
			},
		},
		description: 'The unique identifier of the segment',
	},
	{
		displayName: 'Customer IDs',
		name: 'customerIds',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['segment'],
				operation: ['add', 'remove'],
			},
		},
		description: 'A list of customer IDs to add to the segment',
	},
];
