"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Slack/V1/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Slack/V1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Slack/V1/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Slack/V1/UserDescription.py

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
				name: 'Info',
				value: 'info',
				description: 'Get information about a user',
				action: 'Get information about a user',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get a list of many users',
				action: 'Get many users',
			},
			{
				name: 'Get Presence',
				value: 'getPresence',
				description: 'Get online status of a user',
				action: "Get a user's presence status",
			},
		],
		default: 'info',
	},
];

export const userFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                user:info                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'user',
		type: 'string',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		default: '',
		displayOptions: {
			show: {
				operation: ['info'],
				resource: ['user'],
			},
		},
		required: true,
		description: 'The ID of the user to get information about',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 user:getAll                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['getAll'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 50,
		description: 'Max number of results to return',
	},

	/* -------------------------------------------------------------------------- */
	/*                                user:getPresence                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'user',
		type: 'string',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		default: '',
		displayOptions: {
			show: {
				operation: ['getPresence'],
				resource: ['user'],
			},
		},
		required: true,
		description: 'The ID of the user to get the online status of',
	},
];
