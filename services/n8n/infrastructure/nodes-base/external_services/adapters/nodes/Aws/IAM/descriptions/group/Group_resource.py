"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/descriptions/group/Group.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./get.operation、./getAll.operation 等3项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/descriptions/group/Group.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/descriptions/group/Group_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as update from './update.operation';
import { CURRENT_VERSION } from '../../helpers/constants';
import { handleError } from '../../helpers/errorHandler';
import {
	deleteGroupMembers,
	simplifyGetAllGroupsResponse,
	simplifyGetGroupsResponse,
} from '../../helpers/utils';

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
				action: 'Create group',
				description: 'Create a new group',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'CreateGroup',
							Version: CURRENT_VERSION,
							GroupName: '={{ $parameter["groupName"] }}',
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
				action: 'Delete group',
				description: 'Delete an existing group',
				routing: {
					send: {
						preSend: [deleteGroupMembers],
					},
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'DeleteGroup',
							Version: CURRENT_VERSION,
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
				name: 'Get',
				value: 'get',
				action: 'Get group',
				description: 'Retrieve details of an existing group',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'GetGroup',
							Version: CURRENT_VERSION,
							GroupName: '={{ $parameter["group"] }}',
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError, simplifyGetGroupsResponse],
					},
				},
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many groups',
				description: 'Retrieve a list of groups',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'ListGroups',
							Version: CURRENT_VERSION,
						},
						ignoreHttpStatusErrors: true,
					},
					output: {
						postReceive: [handleError, simplifyGetAllGroupsResponse],
					},
				},
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update group',
				description: 'Update an existing group',
				routing: {
					request: {
						method: 'POST',
						url: '',
						body: {
							Action: 'UpdateGroup',
							Version: CURRENT_VERSION,
							GroupName: '={{ $parameter["group"] }}',
							NewGroupName: '={{ $parameter["groupName"] }}',
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

	...create.description,
	...del.description,
	...get.description,
	...getAll.description,
	...update.description,
];
