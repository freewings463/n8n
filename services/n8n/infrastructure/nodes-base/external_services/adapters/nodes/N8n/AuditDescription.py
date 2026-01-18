"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8n/AuditDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8n 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:auditOperations、auditFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8n/AuditDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8n/AuditDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const auditOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		displayOptions: {
			show: {
				resource: ['audit'],
			},
		},
		options: [
			{
				name: 'Generate',
				value: 'generate',
				action: 'Generate a security audit',
				description: 'Generate a security audit for this n8n instance',
				routing: {
					request: {
						method: 'POST',
						url: '/audit',
					},
				},
			},
		],
	},
];

export const auditFields: INodeProperties[] = [
	{
		displayName: 'Additional Options',
		name: 'additionalOptions',
		type: 'collection',
		placeholder: 'Add Filter',
		displayOptions: {
			show: {
				resource: ['audit'],
			},
		},
		routing: {
			request: {
				body: {
					additionalOptions: '={{ $value }}',
				},
			},
		},
		default: {},
		options: [
			{
				displayName: 'Categories',
				name: 'categories',
				description: 'Risk categories to include in the audit',
				type: 'multiOptions',
				default: [],
				options: [
					{
						name: 'Credentials',
						value: 'credentials',
					},
					{
						name: 'Database',
						value: 'database',
					},
					{
						name: 'Filesystem',
						value: 'filesystem',
					},
					{
						name: 'Instance',
						value: 'instance',
					},
					{
						name: 'Nodes',
						value: 'nodes',
					},
				],
			},
			{
				displayName: 'Days Abandoned Workflow',
				name: 'daysAbandonedWorkflow',
				description: 'Days for a workflow to be considered abandoned if not executed',
				type: 'number',
				default: 90,
			},
		],
	},
];
