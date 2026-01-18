"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8n/ExecutionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8n 的执行节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./WorkflowLocator。导出:executionOperations、executionFields。关键函数/方法:无。用于实现 n8n 执行节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8n/ExecutionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8n/ExecutionDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { getCursorPaginator } from './GenericFunctions';
import { workflowIdLocator } from './WorkflowLocator';

export const executionOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'getAll',
		displayOptions: {
			show: {
				resource: ['execution'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get an execution',
				routing: {
					request: {
						method: 'GET',
						url: '=/executions/{{ $parameter.executionId }}',
					},
				},
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many executions',
				routing: {
					request: {
						method: 'GET',
						url: '/executions',
					},
					send: {
						paginate: true,
					},
					operations: {
						pagination: getCursorPaginator(),
					},
				},
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete an execution',
				routing: {
					request: {
						method: 'DELETE',
						url: '=/executions/{{ $parameter.executionId }}',
					},
				},
			},
		],
	},
];

const deleteOperation: INodeProperties[] = [
	{
		displayName: 'Execution ID',
		name: 'executionId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['execution'],
				operation: ['delete'],
			},
		},
		default: '',
	},
];

const getAllOperation: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['execution'],
				operation: ['getAll'],
			},
		},
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 100,
		typeOptions: {
			minValue: 1,
			maxValue: 250,
		},
		displayOptions: {
			show: {
				resource: ['execution'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		routing: {
			request: {
				qs: {
					limit: '={{ $value }}',
				},
			},
		},
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
				resource: ['execution'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				// Use the common workflowIdLocator, but provide a custom routing
				...workflowIdLocator,
				routing: {
					send: {
						type: 'query',
						property: 'workflowId',
						value: '={{ $value || undefined }}',
					},
				},
				description: 'Workflow to filter the executions by',
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				options: [
					{
						name: 'Error',
						value: 'error',
					},
					{
						name: 'Success',
						value: 'success',
					},
					{
						name: 'Waiting',
						value: 'waiting',
					},
				],
				default: 'success',
				routing: {
					send: {
						type: 'query',
						property: 'status',
						value: '={{ $value }}',
					},
				},
				description: 'Status to filter the executions by',
			},
		],
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add option',
		displayOptions: {
			show: {
				resource: ['execution'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Include Execution Details',
				name: 'activeWorkflows',
				type: 'boolean',
				default: false,
				routing: {
					send: {
						type: 'query',
						property: 'includeData',
						value: '={{ $value }}',
					},
				},
				description: 'Whether to include the detailed execution data',
			},
		],
	},
];

const getOperation: INodeProperties[] = [
	{
		displayName: 'Execution ID',
		name: 'executionId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['execution'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add option',
		displayOptions: {
			show: {
				resource: ['execution'],
				operation: ['get'],
			},
		},
		options: [
			{
				displayName: 'Include Execution Details',
				name: 'activeWorkflows',
				type: 'boolean',
				default: false,
				routing: {
					send: {
						type: 'query',
						property: 'includeData',
						value: '={{ $value }}',
					},
				},
				description: 'Whether to include the detailed execution data',
			},
		],
	},
];

export const executionFields: INodeProperties[] = [
	...deleteOperation,
	...getAllOperation,
	...getOperation,
];
