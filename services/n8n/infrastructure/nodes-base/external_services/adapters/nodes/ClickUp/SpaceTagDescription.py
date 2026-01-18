"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ClickUp/SpaceTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ClickUp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:spaceTagOperations、spaceTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ClickUp/SpaceTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ClickUp/SpaceTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const spaceTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['spaceTag'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a space tag',
				action: 'Create a space tag',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a space tag',
				action: 'Delete a space tag',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many space tags',
				action: 'Get many space tags',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a space tag',
				action: 'Update a space tag',
			},
		],
		default: 'create',
	},
];

export const spaceTagFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                spaceTag:create                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Space ID',
		name: 'space',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['create', 'delete', 'getAll', 'update'],
			},
		},
		required: true,
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['create'],
			},
		},
		required: true,
	},
	{
		displayName: 'Name or ID',
		name: 'name',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsDependsOn: ['space'],
			loadOptionsMethod: 'getTags',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['delete', 'update'],
			},
		},
		required: true,
	},
	{
		displayName: 'New Name',
		name: 'newName',
		type: 'string',
		description: 'New name to set for the tag',
		default: '',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['update'],
			},
		},
		required: true,
	},
	{
		displayName: 'Foreground Color',
		name: 'foregroundColor',
		type: 'color',
		default: '#000000',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['create', 'update'],
			},
		},
		required: true,
	},
	{
		displayName: 'Background Color',
		name: 'backgroundColor',
		type: 'color',
		default: '#000000',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['create', 'update'],
			},
		},
		required: true,
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
				operation: ['getAll'],
			},
		},
		default: true,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['spaceTag'],
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
