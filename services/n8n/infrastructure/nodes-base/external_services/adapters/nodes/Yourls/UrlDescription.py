"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Yourls/UrlDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Yourls 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:urlOperations、urlFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Yourls/UrlDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Yourls/UrlDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const urlOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['url'],
			},
		},
		options: [
			{
				name: 'Expand',
				value: 'expand',
				description: 'Expand a URL',
				action: 'Expand a URL',
			},
			{
				name: 'Shorten',
				value: 'shorten',
				description: 'Shorten a URL',
				action: 'Shorten a URL',
			},
			{
				name: 'Stats',
				value: 'stats',
				description: 'Get stats about one short URL',
				action: 'Get stats for a URL',
			},
		],
		default: 'shorten',
	},
];

export const urlFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                url:shorten                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'URL',
		name: 'url',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['url'],
				operation: ['shorten'],
			},
		},
		default: '',
		description: 'The URL to shorten',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['url'],
				operation: ['shorten'],
			},
		},
		options: [
			{
				displayName: 'Keyword',
				name: 'keyword',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				description: 'Title for custom short URLs',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                url:expand                                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Short URL',
		name: 'shortUrl',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['url'],
				operation: ['expand'],
			},
		},
		default: '',
		description: 'The short URL to expand',
	},

	/* -------------------------------------------------------------------------- */
	/*                                url:stats                                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Short URL',
		name: 'shortUrl',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['url'],
				operation: ['stats'],
			},
		},
		default: '',
		description: 'The short URL for which to get stats',
	},
];
