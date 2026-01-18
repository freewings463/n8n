"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/AwsIam.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./descriptions、./helpers/constants、./helpers/utils、./methods/listSearch。导出:AwsIam。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/AwsIam.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/AwsIam_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { user, group } from './descriptions';
import { BASE_URL } from './helpers/constants';
import { encodeBodyAsFormUrlEncoded } from './helpers/utils';
import { searchGroups, searchUsers, searchGroupsForUser } from './methods/listSearch';

export class AwsIam implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'AWS IAM',
		name: 'awsIam',
		icon: 'file:AwsIam.svg',
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interacts with Amazon IAM',
		defaults: { name: 'AWS IAM' },
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'aws',
				required: true,
			},
		],
		requestDefaults: {
			baseURL: BASE_URL,
			json: true,
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				default: 'user',
				options: [
					{
						name: 'User',
						value: 'user',
					},
					{
						name: 'Group',
						value: 'group',
					},
				],
				routing: {
					send: {
						preSend: [encodeBodyAsFormUrlEncoded],
					},
				},
			},
			...user.description,
			...group.description,
		],
	};

	methods = {
		listSearch: {
			searchGroups,
			searchUsers,
			searchGroupsForUser,
		},
	};
}
