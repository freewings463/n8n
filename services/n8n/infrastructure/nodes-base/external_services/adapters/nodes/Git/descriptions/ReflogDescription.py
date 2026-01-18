"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Git/descriptions/ReflogDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Git/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:reflogFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Git/descriptions/ReflogDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Git/descriptions/ReflogDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const reflogFields: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['reflog'],
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
				operation: ['reflog'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		displayOptions: {
			show: {
				operation: ['reflog'],
			},
		},
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Reference',
				name: 'reference',
				type: 'string',
				default: '',
				placeholder: 'HEAD',
				description:
					'The reference to show the reflog for (e.g., HEAD, branch name). Leave empty for HEAD.',
			},
		],
	},
];
