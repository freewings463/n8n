"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Storyblok/StoryContentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Storyblok 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:storyContentOperations、storyContentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Storyblok/StoryContentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Storyblok/StoryContentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const storyContentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				source: ['contentApi'],
				resource: ['story'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a story',
				action: 'Get a story',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many stories',
				action: 'Get many stories',
			},
		],
		default: 'get',
	},
];

export const storyContentFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                story:get                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Identifier',
		name: 'identifier',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				source: ['contentApi'],
				resource: ['story'],
				operation: ['get'],
			},
		},
		description: 'The ID or slug of the story to get',
	},

	/* -------------------------------------------------------------------------- */
	/*                                story:getAll                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				source: ['contentApi'],
				resource: ['story'],
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
				source: ['contentApi'],
				resource: ['story'],
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
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				source: ['contentApi'],
				resource: ['story'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Starts With',
				name: 'starts_with',
				type: 'string',
				default: '',
				description: 'Filter by slug',
			},
		],
	},
];
