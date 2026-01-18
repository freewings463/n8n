"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/descriptions/user/User.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./addToGroup.operation、./create.operation、./delete.operation、./get.operation 等5项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/descriptions/user/User.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/descriptions/user/User_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as addToGroup from './addToGroup.operation';
import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as removeFromGroup from './removeFromGroup.operation';
import * as update from './update.operation';
import { handleError } from '../../helpers/errorHandler';
import { preSendUserFields, simplifyUser } from '../../helpers/utils';

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
					send: {
						preSend: [preSendUserFields],
					},
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.AdminAddUserToGroup',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'set',
								properties: {
									value: '={{ { "addedToGroup": true } }}',
								},
							},
						],
					},
				},
			},
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new user',
				action: 'Create user',
				routing: {
					send: {
						preSend: [preSendUserFields],
					},
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.AdminCreateUser',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'rootProperty',
								properties: {
									property: 'User',
								},
							},
						],
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
						preSend: [preSendUserFields],
					},
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.AdminDeleteUser',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'set',
								properties: {
									value: '={{ { "deleted": true } }}',
								},
							},
						],
					},
				},
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve information of an existing user',
				action: 'Get user',
				routing: {
					send: {
						preSend: [preSendUserFields],
					},
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.AdminGetUser',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError, simplifyUser],
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
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.ListUsers',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							simplifyUser,
							{
								type: 'rootProperty',
								properties: {
									property: 'Users',
								},
							},
						],
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
					send: {
						preSend: [preSendUserFields],
					},
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.AdminRemoveUserFromGroup',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'set',
								properties: {
									value: '={{ { "removedFromGroup": true } }}',
								},
							},
						],
					},
				},
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an existing user',
				action: 'Update user',
				routing: {
					send: {
						preSend: [preSendUserFields],
					},
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.AdminUpdateUserAttributes',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'set',
								properties: {
									value: '={{ { "updated": true } }}',
								},
							},
						],
					},
				},
			},
		],
	},

	...create.description,
	...del.description,
	...get.description,
	...getAll.description,
	...update.description,
	...addToGroup.description,
	...removeFromGroup.description,
];
