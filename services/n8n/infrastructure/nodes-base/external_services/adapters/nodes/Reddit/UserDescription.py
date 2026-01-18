"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Reddit/UserDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Reddit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:userOperations、userFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Reddit/UserDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Reddit/UserDescription.py

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
				value: 'get',
				action: 'Get a user',
			},
		],
		default: 'get',
	},
];

export const userFields: INodeProperties[] = [
	{
		displayName: 'Username',
		name: 'username',
		type: 'string',
		required: true,
		default: '',
		description: 'Reddit ID of the user to retrieve',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Details',
		name: 'details',
		type: 'options',
		required: true,
		default: 'about',
		description: 'Details of the user to retrieve',
		options: [
			{
				name: 'About',
				value: 'about',
			},
			{
				name: 'Comments',
				value: 'comments',
			},
			{
				name: 'Gilded',
				value: 'gilded',
			},
			{
				name: 'Overview',
				value: 'overview',
			},
			{
				name: 'Submitted',
				value: 'submitted',
			},
		],
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
				details: ['overview', 'submitted', 'comments', 'gilded'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 100,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['get'],
				details: ['comments', 'gilded', 'overview', 'submitted'],
				returnAll: [false],
			},
		},
	},
];
