"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Reddit/SubredditDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Reddit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:subredditOperations、subredditFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Reddit/SubredditDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Reddit/SubredditDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const subredditOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve background information about a subreddit',
				action: 'Get a subreddit',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve information about many subreddits',
				action: 'Get many subreddits',
			},
		],
		displayOptions: {
			show: {
				resource: ['subreddit'],
			},
		},
	},
];

export const subredditFields: INodeProperties[] = [
	// ----------------------------------
	//         subreddit: get
	// ----------------------------------
	{
		displayName: 'Content',
		name: 'content',
		type: 'options',
		required: true,
		default: 'about',
		description: 'Subreddit content to retrieve',
		options: [
			{
				name: 'About',
				value: 'about',
			},
			{
				name: 'Rules',
				value: 'rules',
			},
		],
		displayOptions: {
			show: {
				resource: ['subreddit'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Subreddit',
		name: 'subreddit',
		type: 'string',
		required: true,
		default: '',
		description: 'The name of subreddit to retrieve the content from',
		displayOptions: {
			show: {
				resource: ['subreddit'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------
	//        subreddit: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['subreddit'],
				operation: ['getAll'],
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
				resource: ['subreddit'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Keyword',
				name: 'keyword',
				type: 'string',
				default: '',
				description: 'The keyword for the subreddit search',
			},
			{
				displayName: 'Trending',
				name: 'trending',
				type: 'boolean',
				default: false,
				description: 'Whether to fetch currently trending subreddits in all of Reddit',
			},
		],
		displayOptions: {
			show: {
				resource: ['subreddit'],
				operation: ['getAll'],
			},
		},
	},
];
