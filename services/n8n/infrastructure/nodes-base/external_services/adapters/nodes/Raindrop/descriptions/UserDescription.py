"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Raindrop/descriptions/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Raindrop/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Raindrop/descriptions/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Raindrop/descriptions/UserDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get a user',
			},
		],
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
	},
];

export const userFields: INodeProperties[] = [
	// ----------------------------------
	//          user: get
	// ----------------------------------
	{
		displayName: 'Self',
		name: 'self',
		type: 'boolean',
		default: true,
		required: true,
		description: 'Whether to return details on the logged-in user',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		default: '',
		required: true,
		description: 'The ID of the user to retrieve',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
				self: [false],
			},
		},
	},
];
