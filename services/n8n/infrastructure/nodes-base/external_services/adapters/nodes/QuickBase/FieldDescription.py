"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBase/FieldDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:fieldOperations、fieldFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBase/FieldDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBase/FieldDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const fieldOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['field'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many fields',
				action: 'Get many fields',
			},
		],
		default: 'getAll',
	},
];

export const fieldFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                field:getAll                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Table ID',
		name: 'tableId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['field'],
				operation: ['getAll'],
			},
		},
		description: 'The table identifier',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['field'],
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
				resource: ['field'],
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
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['field'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Include Field Perms',
				name: 'includeFieldPerms',
				type: 'boolean',
				default: false,
				description: 'Whether to get back the custom permissions for the field(s)',
			},
		],
	},
];
