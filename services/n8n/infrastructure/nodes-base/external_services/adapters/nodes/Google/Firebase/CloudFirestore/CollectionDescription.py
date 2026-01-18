"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Firebase/CloudFirestore/CollectionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Firebase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:collectionOperations、collectionFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Firebase/CloudFirestore/CollectionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Firebase/CloudFirestore/CollectionDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const collectionOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['collection'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many root collections',
				action: 'Get many collections',
			},
		],
		default: 'getAll',
	},
];

export const collectionFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                               collection:getAll                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Project Name or ID',
		name: 'projectId',
		type: 'options',
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getProjects',
		},
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['getAll'],
			},
		},
		description:
			'As displayed in firebase console URL. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		required: true,
	},
	{
		displayName: 'Database',
		name: 'database',
		type: 'string',
		default: '(default)',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['getAll'],
			},
		},
		description: 'Usually the provided default value will work',
		required: true,
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['getAll'],
			},
		},
		description: 'Whether to return all results or only up to a given limit',
		required: true,
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['collection'],
				operation: ['getAll'],
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
