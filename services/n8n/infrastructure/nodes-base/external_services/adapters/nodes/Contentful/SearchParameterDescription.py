"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Contentful/SearchParameterDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Contentful 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:fields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Contentful/SearchParameterDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Contentful/SearchParameterDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const fields: INodeProperties[] = [
	{
		displayName: 'Search Parameters',
		name: 'search_parameters',
		description: 'You can use a variety of query parameters to search and filter items',
		placeholder: 'Add parameter',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		options: [
			{
				displayName: 'Parameters',
				name: 'parameters',
				values: [
					{
						displayName: 'Parameter Name',
						name: 'name',
						type: 'string',
						default: '',
						description: 'Name of the search parameter to set',
					},
					{
						displayName: 'Parameter Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the search parameter to set',
					},
				],
			},
		],
	},
];
