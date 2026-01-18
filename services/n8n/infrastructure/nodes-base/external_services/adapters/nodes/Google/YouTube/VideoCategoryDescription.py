"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/YouTube/VideoCategoryDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/YouTube 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:videoCategoryOperations、videoCategoryFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/YouTube/VideoCategoryDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/YouTube/VideoCategoryDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const videoCategoryOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['videoCategory'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many video categories',
				action: 'Get many video categories',
			},
		],
		default: 'getAll',
	},
];

export const videoCategoryFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 videoCategory:getAll                       */
	/* -------------------------------------------------------------------------- */
	{
		// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
		displayName: 'Region Code',
		name: 'regionCode',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['videoCategory'],
			},
		},
		typeOptions: {
			loadOptionsMethod: 'getCountriesCodes',
		},
		default: '',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['videoCategory'],
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
				resource: ['videoCategory'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 50,
		},
		default: 25,
		description: 'Max number of results to return',
	},
];
