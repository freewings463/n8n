"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employee/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create、./get、./getAll、./update。导出:create、get、getAll、update、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employee/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employee/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create';
import * as get from './get';
import * as getAll from './getAll';
import * as update from './update';

export { create, get, getAll, update };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['employee'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an employee',
				action: 'Create an employee',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get an employee',
				action: 'Get an employee',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many employees',
				action: 'Get many employees',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an employee',
				action: 'Update an employee',
			},
		],
		default: 'create',
	},
	...create.description,
	...get.description,
	...getAll.description,
	...update.description,
];
