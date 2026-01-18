"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v1/descriptions/SearchResultDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:searchResultOperations、searchResultFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v1/descriptions/SearchResultDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v1/descriptions/SearchResultDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const searchResultOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['searchResult'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many search results for a search job',
				action: 'Get many search results',
			},
		],
		default: 'getAll',
	},
];

export const searchResultFields: INodeProperties[] = [
	// ----------------------------------------
	//           searchResult: getAll
	// ----------------------------------------
	{
		displayName: 'Search ID',
		name: 'searchJobId',
		description: 'ID of the search whose results to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['searchResult'],
				operation: ['getAll'],
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
				resource: ['searchResult'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['searchResult'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['searchResult'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Key-Value Match',
				name: 'keyValueMatch',
				description:
					'Key-value pair to match against. Example: if "Key" is set to <code>user</code> and "Field" is set to <code>john</code>, only the results where <code>user</code> is <code>john</code> will be returned.',
				type: 'fixedCollection',
				default: {},
				placeholder: 'Add Key-Value Pair',
				options: [
					{
						displayName: 'Key-Value Pair',
						name: 'keyValuePair',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								description: 'Key to match against',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Value',
								name: 'value',
								description: 'Value to match against',
								type: 'string',
								default: '',
							},
						],
					},
				],
			},
		],
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				resource: ['searchResult'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Add Summary to Metadata',
				name: 'add_summary_to_metadata',
				description: 'Whether to include field summary statistics in the response',
				type: 'boolean',
				default: false,
			},
		],
	},
];
