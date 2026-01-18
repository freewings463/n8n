"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/query/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./executeQuery.operation。导出:executeQuery、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/query/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/query/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as executeQuery from './executeQuery.operation';

export { executeQuery };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		noDataExpression: true,
		type: 'options',
		required: true,
		default: 'executeQuery',
		options: [
			{
				name: 'Execute Query',
				value: 'executeQuery',
				action: 'Execute a query',
			},
		],
		displayOptions: {
			show: {
				resource: ['query'],
			},
		},
	},
	...executeQuery.description,
];
