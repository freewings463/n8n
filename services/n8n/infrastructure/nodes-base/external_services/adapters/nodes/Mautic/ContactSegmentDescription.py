"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mautic/ContactSegmentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mautic 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactSegmentOperations、contactSegmentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mautic/ContactSegmentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mautic/ContactSegmentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const contactSegmentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['contactSegment'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add contact to a segment',
				action: 'Add a contact to a segment',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove contact from a segment',
				action: 'Remove a contact from a segment',
			},
		],
		default: 'add',
	},
];

export const contactSegmentFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                               contactSegment:add                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactSegment'],
				operation: ['add', 'remove'],
			},
		},
		default: '',
	},
	{
		displayName: 'Segment Name or ID',
		name: 'segmentId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		displayOptions: {
			show: {
				resource: ['contactSegment'],
				operation: ['add', 'remove'],
			},
		},
		typeOptions: {
			loadOptionsMethod: 'getSegments',
		},
		default: '',
	},
];
