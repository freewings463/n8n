"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/alert/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./getMetrics.operation、./getReport.operation。导出:getReport、getMetrics、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/alert/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/alert/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as getMetrics from './getMetrics.operation';
import * as getReport from './getReport.operation';

export { getReport, getMetrics };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['alert'],
			},
		},
		options: [
			{
				name: 'Get Fired Alerts',
				value: 'getReport',
				description: 'Retrieve a fired alerts report',
				action: 'Get a fired alerts report',
			},
			{
				name: 'Get Metrics',
				value: 'getMetrics',
				description: 'Retrieve metrics',
				action: 'Get metrics',
			},
		],
		default: 'getReport',
	},

	...getReport.description,
	...getMetrics.description,
];
