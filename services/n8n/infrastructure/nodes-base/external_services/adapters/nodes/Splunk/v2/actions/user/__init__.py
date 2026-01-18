"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/user/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteUser.operation、./get.operation、./getAll.operation 等1项。导出:create、deleteUser、get、getAll、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/user/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/user/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteUser from './deleteUser.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as update from './update.operation';

export { create, deleteUser, get, getAll, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an user',
				action: 'Create a user',
			},
			{
				name: 'Delete',
				value: 'deleteUser',
				description: 'Delete an user',
				action: 'Delete a user',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve an user',
				action: 'Get a user',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many users',
				action: 'Get many users',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an user',
				action: 'Update a user',
			},
		],
		default: 'create',
	},

	...create.description,
	...deleteUser.description,
	...get.description,
	...getAll.description,
	...update.description,
];
