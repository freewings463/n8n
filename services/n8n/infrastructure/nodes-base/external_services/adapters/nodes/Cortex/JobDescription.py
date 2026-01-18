"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cortex/JobDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cortex 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:jobOperations、jobFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cortex/JobDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cortex/JobDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const jobOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		description: 'Choose an operation',
		required: true,
		displayOptions: {
			show: {
				resource: ['job'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get job details',
				action: 'Get a job',
			},
			{
				name: 'Report',
				value: 'report',
				description: 'Get job report',
				action: 'Get a job report',
			},
		],
		default: 'get',
	},
];

export const jobFields: INodeProperties[] = [
	{
		displayName: 'Job ID',
		name: 'jobId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['job'],
				operation: ['get', 'report'],
			},
		},
		default: '',
		description: 'ID of the job',
	},
];
