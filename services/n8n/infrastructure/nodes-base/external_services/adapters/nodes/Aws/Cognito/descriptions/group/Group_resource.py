"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/descriptions/group/Group.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./get.operation、./getAll.operation 等3项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/descriptions/group/Group.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/descriptions/group/Group_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as update from './update.operation';
import { handleError } from '../../helpers/errorHandler';
import { processGroup } from '../../helpers/utils';

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'getAll',
		displayOptions: {
			show: {
				resource: ['group'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new group',
				routing: {
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.CreateGroup',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'rootProperty',
								properties: {
									property: 'Group',
								},
							},
						],
					},
				},
				action: 'Create group',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an existing group',
				routing: {
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.DeleteGroup',
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
				action: 'Delete group',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve details of an existing group',
				routing: {
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.GetGroup',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError, processGroup],
					},
				},
				action: 'Get group',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve a list of groups',
				routing: {
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.ListGroups',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [
							handleError,
							processGroup,
							{
								type: 'rootProperty',
								properties: {
									property: 'Groups',
								},
							},
						],
					},
				},
				action: 'Get many groups',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an existing group',
				routing: {
					request: {
						method: 'POST',
						headers: {
							'X-Amz-Target': 'AWSCognitoIdentityProviderService.UpdateGroup',
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
				action: 'Update group',
			},
		],
	},

	...create.description,
	...del.description,
	...get.description,
	...getAll.description,
	...update.description,
];
