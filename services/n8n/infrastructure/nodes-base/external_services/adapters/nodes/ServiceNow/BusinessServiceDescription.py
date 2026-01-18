"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ServiceNow/BusinessServiceDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ServiceNow 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:businessServiceOperations、businessServiceFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ServiceNow/BusinessServiceDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ServiceNow/BusinessServiceDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const businessServiceOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['businessService'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many business services',
			},
		],
		default: 'getAll',
	},
];

export const businessServiceFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                businessService:getAll                      */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['businessService'],
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
				operation: ['getAll'],
				resource: ['businessService'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 50,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['businessService'],
				operation: ['getAll'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Exclude Reference Link',
				name: 'sysparm_exclude_reference_link',
				type: 'boolean',
				default: false,
				description: 'Whether to exclude Table API links for reference fields',
			},
			{
				displayName: 'Field Names or IDs',
				name: 'sysparm_fields',
				type: 'multiOptions',
				typeOptions: {
					// nodelinter-ignore-next-line
					loadOptionsMethod: 'getColumns',
				},
				default: [],
				description:
					'A list of fields to return. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
				hint: 'String of comma separated values or an array of strings can be set in an expression',
			},
			{
				displayName: 'Filter',
				name: 'sysparm_query',
				type: 'string',
				default: '',
				description:
					'An encoded query string used to filter the results. <a href="https://developer.servicenow.com/dev.do#!/learn/learning-plans/quebec/servicenow_application_developer/app_store_learnv2_rest_quebec_more_about_query_parameters">More info</a>.',
			},
			{
				displayName: 'Return Values',
				name: 'sysparm_display_value',
				type: 'options',
				options: [
					{
						name: 'Actual Values',
						value: 'false',
					},
					{
						name: 'Both',
						value: 'all',
					},
					{
						name: 'Display Values',
						value: 'true',
					},
				],
				default: 'false',
				description: 'Choose which values to return',
			},
		],
	},
];
