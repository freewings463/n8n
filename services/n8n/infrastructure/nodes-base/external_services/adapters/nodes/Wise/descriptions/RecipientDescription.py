"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wise/descriptions/RecipientDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wise/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:recipientOperations、recipientFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wise/descriptions/RecipientDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wise/descriptions/RecipientDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const recipientOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'getAll',
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many recipients',
			},
		],
		displayOptions: {
			show: {
				resource: ['recipient'],
			},
		},
	},
];

export const recipientFields: INodeProperties[] = [
	// ----------------------------------
	//        recipient: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['recipient'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 5,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		displayOptions: {
			show: {
				resource: ['recipient'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
];
