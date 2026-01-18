"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Analytics/v2/actions/report/Report.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Analytics 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./get.ga4.operation、./get.universal.operation。导出:getga4、getuniversal、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Analytics/v2/actions/report/Report.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Analytics/v2/actions/report/Report_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as getga4 from './get.ga4.operation';
import * as getuniversal from './get.universal.operation';

export { getga4, getuniversal };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['report'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Return the analytics data',
				action: 'Get a report',
			},
		],
		default: 'get',
	},
	{
		displayName: 'Property Type',
		name: 'propertyType',
		type: 'options',
		noDataExpression: true,
		description:
			'Google Analytics 4 is the latest version. Universal Analytics is an older version that is not fully functional after the end of June 2023.',
		options: [
			{
				name: 'Google Analytics 4',
				value: 'ga4',
			},
			{
				name: 'Universal Analytics',
				value: 'universal',
			},
		],
		default: 'ga4',
		displayOptions: {
			show: {
				resource: ['report'],
				operation: ['get'],
			},
		},
	},
	...getga4.description,
	...getuniversal.description,
];
