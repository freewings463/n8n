"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/descriptions/user/User.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./addToGroup.operation、./create.operation、./delete.operation、./get.operation 等6项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/descriptions/user/User.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/descriptions/user/User_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as addToGroup from './addToGroup.operation';
import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as removeFromGroup from './removeFromGroup.operation';
import * as update from './update.operation';
import { CURRENT_VERSION } from '../../helpers/constants';
import { handleError } from '../../helpers/errorHandler';
import { removeUserFromGroups, simplifyGetAllUsersResponse } from '../../helpers/utils';

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'getAll',
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
		options: [
			{
				name: 'Add to Group',
				value: 'addToGroup',
				description: 'Add an existing user to a group',
				action: 'Add user to group',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'AddUserToGroup',
							Version: CURRENT_VERSION,
							UserName: '={{ $parameter["user"] }}',
							GroupName: '={{ $parameter["group"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError],
					},
				},
			},
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new user',
				action: 'Create user',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'CreateUser',
							Version: CURRENT_VERSION,
							UserName: '={{ $parameter["userName"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError],
					},
				},
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a user',
				action: 'Delete user',
				routing: {
					send: {
						preSend: [removeUserFromGroups],
					},
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'DeleteUser',
							Version: CURRENT_VERSION,
							UserName: '={{ $parameter["user"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError],
					},
				},
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a user',
				action: 'Get user',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'GetUser',
							Version: CURRENT_VERSION,
							UserName: '={{ $parameter["user"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							{
								type: 'rootProperty',
								properties: {
									property: 'GetUserResponse.GetUserResult.User',
								},
							},
							handleError,
						],
					},
				},
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve a list of users',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'ListUsers',
							Version: CURRENT_VERSION,
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError, simplifyGetAllUsersResponse],
					},
				},
				action: 'Get many users',
			},
			{
				name: 'Remove From Group',
				value: 'removeFromGroup',
				description: 'Remove a user from a group',
				action: 'Remove user from group',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'RemoveUserFromGroup',
							Version: CURRENT_VERSION,
							UserName: '={{ $parameter["user"] }}',
							GroupName: '={{ $parameter["group"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError],
					},
				},
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a user',
				action: 'Update user',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'UpdateUser',
							Version: CURRENT_VERSION,
							NewUserName: '={{ $parameter["userName"] }}',
							UserName: '={{ $parameter["user"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError],
					},
				},
			},
		],
	},

	...addToGroup.description,
	...create.description,
	...del.description,
	...get.description,
	...getAll.description,
	...update.description,
	...removeFromGroup.description,
];
