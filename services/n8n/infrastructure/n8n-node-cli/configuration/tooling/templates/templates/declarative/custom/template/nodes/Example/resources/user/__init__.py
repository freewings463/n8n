"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/custom/template/nodes/Example/resources/user/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create、./get。导出:userDescription。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/custom/template/nodes/Example/resources/user/index.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/custom/template/nodes/Example/resources/user/__init__.py

import type { INodeProperties } from 'n8n-workflow';
import { userCreateDescription } from './create';
import { userGetDescription } from './get';

const showOnlyForUsers = {
	resource: ['user'],
};

export const userDescription: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: showOnlyForUsers,
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get users',
				description: 'Get many users',
				routing: {
					request: {
						method: 'GET',
						url: '/users',
					},
				},
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a user',
				description: 'Get the data of a single user',
				routing: {
					request: {
						method: 'GET',
						url: '=/users/{{$parameter.userId}}',
					},
				},
			},
			{
				name: 'Create',
				value: 'create',
				action: 'Create a new user',
				description: 'Create a new user',
				routing: {
					request: {
						method: 'POST',
						url: '/users',
					},
				},
			},
		],
		default: 'getAll',
	},
	...userGetDescription,
	...userCreateDescription,
];
