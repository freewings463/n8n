"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cockpit/SingletonDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cockpit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:singletonOperations、singletonFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cockpit/SingletonDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cockpit/SingletonDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const singletonOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['singleton'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a singleton',
				action: 'Get a singleton',
			},
		],
		default: 'get',
	},
];

export const singletonFields: INodeProperties[] = [
	{
		displayName: 'Singleton Name or ID',
		name: 'singleton',
		type: 'options',
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getSingletons',
		},
		displayOptions: {
			show: {
				resource: ['singleton'],
			},
		},
		required: true,
		description:
			'Name of the singleton to operate on. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
];
