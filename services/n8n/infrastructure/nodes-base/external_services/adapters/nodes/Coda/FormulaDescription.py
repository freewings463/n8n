"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Coda/FormulaDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Coda 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:formulaOperations、formulaFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Coda/FormulaDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Coda/FormulaDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const formulaOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['formula'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a formula',
				action: 'Get a formula',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many formulas',
				action: 'Get many formulas',
			},
		],
		default: 'get',
	},
];

export const formulaFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                   formula:get                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Doc Name or ID',
		name: 'docId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getDocs',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['formula'],
				operation: ['get'],
			},
		},
		description:
			'ID of the doc. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Formula ID',
		name: 'formulaId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['formula'],
				operation: ['get'],
			},
		},
		description: 'The formula to get the row from',
	},
	/* -------------------------------------------------------------------------- */
	/*                                   formula:getAll                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Doc Name or ID',
		name: 'docId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getDocs',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['formula'],
				operation: ['getAll'],
			},
		},
		description:
			'ID of the doc. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['formula'],
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
				resource: ['formula'],
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
];
