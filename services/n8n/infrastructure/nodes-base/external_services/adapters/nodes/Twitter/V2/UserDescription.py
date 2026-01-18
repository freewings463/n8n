"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Twitter/V2/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Twitter/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Twitter/V2/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Twitter/V2/UserDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userOperations: INodeProperties[] = [
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
				name: 'Get',
				value: 'searchUser',
				description: 'Retrieve a user by username',
				action: 'Get User',
			},
		],
		default: 'searchUser',
	},
];

export const userFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                user:searchUser                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User',
		name: 'user',
		type: 'resourceLocator',
		default: { mode: 'username', value: '' },
		required: true,
		description: 'The user you want to search',
		displayOptions: {
			show: {
				operation: ['searchUser'],
				resource: ['user'],
			},
			hide: {
				me: [true],
			},
		},
		modes: [
			{
				displayName: 'By Username',
				name: 'username',
				type: 'string',
				validation: [],
				placeholder: 'e.g. n8n',
				url: '',
			},
			{
				displayName: 'By ID',
				name: 'id',
				type: 'string',
				validation: [],
				placeholder: 'e.g. 1068479892537384960',
				url: '',
			},
		],
	},
	{
		displayName: 'Me',
		name: 'me',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['searchUser'],
				resource: ['user'],
			},
		},
		default: false,
		description: 'Whether you want to search the authenticated user',
	},
];
