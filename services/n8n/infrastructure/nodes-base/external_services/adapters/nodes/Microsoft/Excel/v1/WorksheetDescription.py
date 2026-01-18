"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v1/WorksheetDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:worksheetOperations、worksheetFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v1/WorksheetDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v1/WorksheetDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const worksheetOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['worksheet'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many worksheets',
				action: 'Get many worksheets',
			},
			{
				name: 'Get Content',
				value: 'getContent',
				description: 'Get worksheet content',
				action: 'Get a worksheet',
			},
		],
		default: 'create',
	},
];

export const worksheetFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 worksheet:getAll                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Workbook Name or ID',
		name: 'workbook',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getWorkbooks',
		},
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['worksheet'],
			},
		},
		default: '',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['worksheet'],
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
				resource: ['worksheet'],
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
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['worksheet'],
			},
		},
		options: [
			{
				displayName: 'Fields',
				name: 'fields',
				type: 'string',
				default: '',
				description: 'Fields the response will containt. Multiple can be added separated by ,.',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                 worksheet:getContent                       */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Workbook Name or ID',
		name: 'workbook',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getWorkbooks',
		},
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
			},
		},
		default: '',
	},
	{
		displayName: 'Worksheet Name or ID',
		name: 'worksheet',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getworksheets',
			loadOptionsDependsOn: ['workbook'],
		},
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
			},
		},
		default: '',
	},
	{
		displayName: 'Range',
		name: 'range',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
			},
		},
		default: 'A1:C3',
		required: true,
		description:
			'The address or the name of the range. If not specified, the entire worksheet range is returned.',
	},
	{
		displayName: 'RAW Data',
		name: 'rawData',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
			},
		},
		default: false,
		description:
			'Whether the data should be returned RAW instead of parsed into keys according to their header',
	},
	{
		displayName: 'Data Property',
		name: 'dataProperty',
		type: 'string',
		default: 'data',
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
				rawData: [true],
			},
		},
		description: 'The name of the property into which to write the RAW data',
	},
	{
		displayName: 'Data Start Row',
		name: 'dataStartRow',
		type: 'number',
		typeOptions: {
			minValue: 1,
		},
		default: 1,
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
			},
			hide: {
				rawData: [true],
			},
		},
		description:
			'Index of the first row which contains the actual data and not the keys. Starts with 0.',
	},
	{
		displayName: 'Key Row',
		name: 'keyRow',
		type: 'number',
		typeOptions: {
			minValue: 0,
		},
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
			},
			hide: {
				rawData: [true],
			},
		},
		default: 0,
		description:
			'Index of the row which contains the keys. Starts at 0. The incoming node data is matched to the keys for assignment. The matching is case sensitve.',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				operation: ['getContent'],
				resource: ['worksheet'],
				rawData: [true],
			},
		},
		options: [
			{
				displayName: 'Fields',
				name: 'fields',
				type: 'string',
				default: '',
				description: 'Fields the response will containt. Multiple can be added separated by ,.',
			},
		],
	},
];
