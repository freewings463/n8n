"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ConvertKit/CustomFieldDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ConvertKit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:customFieldOperations、customFieldFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ConvertKit/CustomFieldDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ConvertKit/CustomFieldDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const customFieldOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['customField'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a field',
				action: 'Create a custom field',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a field',
				action: 'Delete a custom field',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many fields',
				action: 'Get many custom fields',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a field',
				action: 'Update a custom field',
			},
		],
		default: 'update',
	},
];

export const customFieldFields: INodeProperties[] = [
	{
		displayName: 'Field ID',
		name: 'id',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['customField'],
				operation: ['update', 'delete'],
			},
		},
		default: '',
		description: 'The ID of your custom field',
	},
	{
		displayName: 'Label',
		name: 'label',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['customField'],
				operation: ['update', 'create'],
			},
		},
		default: '',
		description: 'The label of the custom field',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['customField'],
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
				resource: ['customField'],
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
];
