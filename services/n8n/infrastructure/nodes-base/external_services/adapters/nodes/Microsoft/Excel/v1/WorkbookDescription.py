"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v1/WorkbookDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:workbookOperations、workbookFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v1/WorkbookDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v1/WorkbookDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const workbookOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['workbook'],
			},
		},
		options: [
			{
				name: 'Add Worksheet',
				value: 'addWorksheet',
				description: 'Adds a new worksheet to the workbook',
				action: 'Add a worksheet to a workbook',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get data of many workbooks',
				action: 'Get many workbooks',
			},
		],
		default: 'create',
	},
];

export const workbookFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 workbook:addWorksheet                      */
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
				operation: ['addWorksheet'],
				resource: ['workbook'],
			},
		},
		default: '',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['addWorksheet'],
				resource: ['workbook'],
			},
		},
		options: [
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description:
					'The name of the worksheet to be added. If specified, name should be unqiue. If not specified, Excel determines the name of the new worksheet.',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                 workbook:getAll                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['workbook'],
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
				resource: ['workbook'],
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
				resource: ['workbook'],
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
