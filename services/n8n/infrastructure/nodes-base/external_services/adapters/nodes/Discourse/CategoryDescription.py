"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discourse/CategoryDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discourse 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:categoryOperations、categoryFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discourse/CategoryDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discourse/CategoryDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const categoryOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		description: 'Choose an operation',
		required: true,
		displayOptions: {
			show: {
				resource: ['category'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a category',
				action: 'Create a category',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many categories',
				action: 'Get many categories',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a category',
				action: 'Update a category',
			},
		],
		default: 'create',
	},
];

export const categoryFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                category:create                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['category'],
				operation: ['create'],
			},
		},
		default: '',
		description: 'Name of the category',
	},
	{
		displayName: 'Color',
		name: 'color',
		type: 'color',
		required: true,
		displayOptions: {
			show: {
				resource: ['category'],
				operation: ['create'],
			},
		},
		default: '0000FF',
		description: 'Color of the category',
	},
	{
		displayName: 'Text Color',
		name: 'textColor',
		type: 'color',
		required: true,
		displayOptions: {
			show: {
				resource: ['category'],
				operation: ['create'],
			},
		},
		default: '0000FF',
		description: 'Text color of the category',
	},

	/* -------------------------------------------------------------------------- */
	/*                                category:getAll                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['category'],
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
				resource: ['category'],
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

	/* -------------------------------------------------------------------------- */
	/*                                category:update                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Category ID',
		name: 'categoryId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['category'],
				operation: ['update'],
			},
		},
		default: '',
		description: 'ID of the category',
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['category'],
				operation: ['update'],
			},
		},
		default: '',
		description: 'New name of the category',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['category'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Color',
				name: 'color',
				type: 'color',
				default: '0000FF',
				description: 'Color of the category',
			},
			{
				displayName: 'Text Color',
				name: 'textColor',
				type: 'color',
				default: '0000FF',
				description: 'Text color of the category',
			},
		],
	},
];
