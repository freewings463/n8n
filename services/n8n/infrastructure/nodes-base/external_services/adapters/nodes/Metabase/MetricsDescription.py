"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Metabase/MetricsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Metabase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:metricsOperations、metricsFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Metabase/MetricsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Metabase/MetricsDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const metricsOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['metrics'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a specific metric',
				routing: {
					request: {
						method: 'GET',
						url: '={{"/api/metric/" + $parameter.metricId}}',
						returnFullResponse: true,
					},
				},
				action: 'Get a metric',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many metrics',
				routing: {
					request: {
						method: 'GET',
						url: '/api/metric/',
					},
				},
				action: 'Get many metrics',
			},
		],
		default: 'getAll',
	},
];

export const metricsFields: INodeProperties[] = [
	{
		displayName: 'Metric ID',
		name: 'metricId',
		type: 'string',
		required: true,
		placeholder: '0',
		displayOptions: {
			show: {
				resource: ['metrics'],
				operation: ['get'],
			},
		},
		default: '',
	},
];
