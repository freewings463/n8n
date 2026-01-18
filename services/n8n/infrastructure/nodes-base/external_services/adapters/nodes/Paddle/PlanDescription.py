"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Paddle/PlanDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Paddle 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:planOperations、planFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Paddle/PlanDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Paddle/PlanDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const planOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['plan'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a plan',
				action: 'Get a plan',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many plans',
				action: 'Get many plans',
			},
		],
		default: 'get',
	},
];

export const planFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 plan:get                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Plan ID',
		name: 'planId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['plan'],
				operation: ['get'],
			},
		},
		description: 'Filter: The subscription plan ID',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['plan'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['plan'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
