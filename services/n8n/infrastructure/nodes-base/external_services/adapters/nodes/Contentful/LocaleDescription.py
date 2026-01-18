"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Contentful/LocaleDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Contentful 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:resource、operations、fields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Contentful/LocaleDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Contentful/LocaleDescription.py

import type { INodeProperties, INodePropertyOptions } from 'n8n-workflow';

export const resource = {
	name: 'Locale',
	value: 'locale',
} as INodePropertyOptions;

export const operations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: [resource.value],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
			},
		],
		default: 'getAll',
	},
];

export const fields: INodeProperties[] = [
	{
		displayName: 'Environment ID',
		name: 'environmentId',
		type: 'string',
		displayOptions: {
			show: {
				resource: [resource.value],
				operation: ['get', 'getAll'],
			},
		},
		default: 'master',
		description:
			'The ID for the Contentful environment (e.g. master, staging, etc.). Depending on your plan, you might not have environments. In that case use "master".',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: [resource.value],
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
				resource: [resource.value],
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
