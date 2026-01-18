"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Metabase/AlertsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Metabase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:alertsOperations、alertsFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Metabase/AlertsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Metabase/AlertsDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const alertsOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['alerts'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get specific alert',
				routing: {
					request: {
						method: 'GET',
						url: '={{"/api/alert/" + $parameter.alertId}}',
					},
				},
				action: 'Get an alert',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many alerts',
				routing: {
					request: {
						method: 'GET',
						url: '/api/alert/',
					},
				},
				action: 'Get many alerts',
			},
		],
		default: 'getAll',
	},
];

export const alertsFields: INodeProperties[] = [
	{
		displayName: 'Alert ID',
		name: 'alertId',
		type: 'string',
		required: true,
		placeholder: '0',
		displayOptions: {
			show: {
				resource: ['alerts'],
				operation: ['get'],
			},
		},
		default: '',
	},
];
