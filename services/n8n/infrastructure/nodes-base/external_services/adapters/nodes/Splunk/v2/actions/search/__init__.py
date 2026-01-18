"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/search/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteJob.operation、./get.operation、./getAll.operation 等1项。导出:create、deleteJob、get、getAll、getResult、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/search/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/search/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteJob from './deleteJob.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as getResult from './getResult.operation';

export { create, deleteJob, get, getAll, getResult };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['search'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a search job',
				action: 'Create a search job',
			},
			{
				name: 'Delete',
				value: 'deleteJob',
				description: 'Delete a search job',
				action: 'Delete a search job',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a search job',
				action: 'Get a search job',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many search jobs',
				action: 'Get many search jobs',
			},
			{
				name: 'Get Result',
				value: 'getResult',
				description: 'Get the result of a search job',
				action: 'Get the result of a search job',
			},
		],
		default: 'create',
	},

	...create.description,
	...deleteJob.description,
	...get.description,
	...getAll.description,
	...getResult.description,
];
