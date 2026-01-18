"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Keap/ContactTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Keap 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactTagOperations、contactTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Keap/ContactTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Keap/ContactTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const contactTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['contactTag'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Add a list of tags to a contact',
				action: 'Create a contact tag',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: "Delete a contact's tag",
				action: 'Delete a contact tag',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: "Retrieve many contact's tags",
				action: 'Get many contact tags',
			},
		],
		default: 'create',
	},
];

export const contactTagFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 contactTag:create                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['contactTag'],
			},
		},
		default: '',
	},
	{
		displayName: 'Tag Names or IDs',
		name: 'tagIds',
		type: 'multiOptions',
		description:
			'Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['contactTag'],
			},
		},
		default: [],
	},
	/* -------------------------------------------------------------------------- */
	/*                                 contactTag:delete                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['contactTag'],
			},
		},
		default: '',
	},
	{
		displayName: 'Tag IDs',
		name: 'tagIds',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['contactTag'],
			},
		},
		default: 'Tag IDs, multiple IDs can be set separated by comma.',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 contactTag:getAll                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['contactTag'],
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
				resource: ['contactTag'],
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
				resource: ['contactTag'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 200,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
