"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/report/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteReport.operation、./get.operation、./getAll.operation。导出:create、deleteReport、get、getAll、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/report/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/report/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteReport from './deleteReport.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';

export { create, deleteReport, get, getAll };

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
				name: 'Create From Search',
				value: 'create',
				description: 'Create a search report from a search job',
				action: 'Create a search report',
			},
			{
				name: 'Delete',
				value: 'deleteReport',
				description: 'Delete a search report',
				action: 'Delete a search report',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a search report',
				action: 'Get a search report',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many search reports',
				action: 'Get many search reports',
			},
		],
		default: 'getAll',
	},

	...create.description,
	...deleteReport.description,
	...get.description,
	...getAll.description,
];
