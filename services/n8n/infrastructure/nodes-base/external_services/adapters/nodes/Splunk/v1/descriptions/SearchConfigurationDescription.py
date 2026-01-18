"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v1/descriptions/SearchConfigurationDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:searchConfigurationOperations、searchConfigurationFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v1/descriptions/SearchConfigurationDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v1/descriptions/SearchConfigurationDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const searchConfigurationOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['searchConfiguration'],
			},
		},
		options: [
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a search configuration',
				action: 'Delete a search configuration',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a search configuration',
				action: 'Get a search configuration',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many search configurations',
				action: 'Get many search configurations',
			},
		],
		default: 'delete',
	},
];

export const searchConfigurationFields: INodeProperties[] = [
	// ----------------------------------------
	//       searchConfiguration: delete
	// ----------------------------------------
	{
		displayName: 'Search Configuration ID',
		name: 'searchConfigurationId',
		description: 'ID of the search configuration to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['searchConfiguration'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//         searchConfiguration: get
	// ----------------------------------------
	{
		displayName: 'Search Configuration ID',
		name: 'searchConfigurationId',
		description: 'ID of the search configuration to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['searchConfiguration'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//       searchConfiguration: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['searchConfiguration'],
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
				resource: ['searchConfiguration'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				resource: ['searchConfiguration'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Add Orphan Field',
				name: 'add_orphan_field',
				description:
					'Whether to include a boolean value for each saved search to show whether the search is orphaned, meaning that it has no valid owner',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'List Default Actions',
				name: 'listDefaultActionArgs',
				type: 'boolean',
				default: false,
			},
		],
	},
];
