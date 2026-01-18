"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/fileFolder/FileFolder.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./search.operation。导出:search、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/fileFolder/FileFolder.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/fileFolder/FileFolder_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as search from './search.operation';

export { search };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['fileFolder'],
			},
		},
		options: [
			{
				name: 'Search',
				value: 'search',
				description: 'Search or list files and folders',
				action: 'Search files and folders',
			},
		],
		default: 'search',
	},
	...search.description,
];
