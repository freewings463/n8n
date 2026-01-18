"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Harvest/CompanyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Harvest 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:companyOperations。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Harvest/CompanyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Harvest/CompanyDescription.py

import type { INodeProperties } from 'n8n-workflow';

const resource = ['company'];

export const companyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource,
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieves the company for the currently authenticated user',
				action: 'Retrieve the company for the currently authenticated user',
			},
		],
		default: 'get',
	},
];
