"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Analytics/v1/UserActivityDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Analytics 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userActivityOperations、userActivityFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Analytics/v1/UserActivityDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Analytics/v1/UserActivityDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const userActivityOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['userActivity'],
			},
		},
		options: [
			{
				name: 'Search',
				value: 'search',
				description: 'Return user activity data',
				action: 'Search user activity data',
			},
		],
		default: 'search',
	},
];

export const userActivityFields: INodeProperties[] = [
	{
		displayName: 'View Name or ID',
		name: 'viewId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getViews',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['userActivity'],
				operation: ['search'],
			},
		},
		placeholder: '123456',
		description:
			'The View ID of Google Analytics. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['userActivity'],
				operation: ['search'],
			},
		},
		placeholder: '123456',
		description: 'ID of a user',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['search'],
				resource: ['userActivity'],
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
				operation: ['search'],
				resource: ['userActivity'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['search'],
				resource: ['userActivity'],
			},
		},
		options: [
			{
				displayName: 'Activity Types',
				name: 'activityTypes',
				type: 'multiOptions',
				options: [
					{
						name: 'Ecommerce',
						value: 'ECOMMERCE',
					},
					{
						name: 'Event',
						value: 'EVENT',
					},
					{
						name: 'Goal',
						value: 'GOAL',
					},
					{
						name: 'Pageview',
						value: 'PAGEVIEW',
					},
					{
						name: 'Screenview',
						value: 'SCREENVIEW',
					},
				],
				description: 'Type of activites requested',
				default: [],
			},
		],
	},
];
