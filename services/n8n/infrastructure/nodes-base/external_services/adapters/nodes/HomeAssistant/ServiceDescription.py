"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HomeAssistant/ServiceDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HomeAssistant 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:serviceOperations、serviceFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HomeAssistant/ServiceDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HomeAssistant/ServiceDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const serviceOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['service'],
			},
		},
		options: [
			{
				name: 'Call',
				value: 'call',
				description: 'Call a service within a specific domain',
				action: 'Call a service',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many services',
				action: 'Get many services',
			},
		],
		default: 'getAll',
	},
];

export const serviceFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                service:getAll                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['service'],
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
				resource: ['service'],
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
	/*                                service:Call                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Domain Name or ID',
		name: 'domain',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getDomains',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['service'],
				operation: ['call'],
			},
		},
	},
	{
		displayName: 'Service Name or ID',
		name: 'service',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsDependsOn: ['domain'],
			loadOptionsMethod: 'getDomainServices',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['service'],
				operation: ['call'],
			},
		},
	},
	{
		displayName: 'Service Attributes',
		name: 'serviceAttributes',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		placeholder: 'Add Attribute',
		default: {},
		displayOptions: {
			show: {
				resource: ['service'],
				operation: ['call'],
			},
		},
		options: [
			{
				name: 'attributes',
				displayName: 'Attributes',
				values: [
					{
						displayName: 'Name',
						name: 'name',
						type: 'string',
						default: '',
						description: 'Name of the field',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the field',
					},
				],
			},
		],
	},
];
