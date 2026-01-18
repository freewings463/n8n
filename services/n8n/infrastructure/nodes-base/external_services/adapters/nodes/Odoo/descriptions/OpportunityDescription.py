"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Odoo/descriptions/OpportunityDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Odoo/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:opportunityOperations、opportunityDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Odoo/descriptions/OpportunityDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Odoo/descriptions/OpportunityDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const opportunityOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		default: 'create',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['opportunity'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new opportunity',
				action: 'Create an opportunity',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an opportunity',
				action: 'Delete an opportunity',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get an opportunity',
				action: 'Get an opportunity',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many opportunities',
				action: 'Get many opportunities',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an opportunity',
				action: 'Update an opportunity',
			},
		],
	},
];

export const opportunityDescription: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                opportunity:create                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'opportunityName',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['opportunity'],
			},
		},
	},

	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['opportunity'],
			},
		},
		options: [
			{
				displayName: 'Email',
				name: 'email_from',
				type: 'string',
				default: '',
			},
			// {
			// 	displayName: 'Expected Closing Date',
			// 	name: 'date_deadline',
			// 	type: 'dateTime',
			// 	default: '',
			// },
			{
				displayName: 'Expected Revenue',
				name: 'expected_revenue',
				type: 'number',
				default: 0,
			},
			{
				displayName: 'Internal Notes',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Phone',
				name: 'phone',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Priority',
				name: 'priority',
				type: 'options',
				default: '1',
				options: [
					{
						name: '1',
						value: '1',
					},
					{
						name: '2',
						value: '2',
					},
					{
						name: '3',
						value: '3',
					},
				],
			},
			{
				displayName: 'Probability',
				name: 'probability',
				type: 'number',
				default: 0,
				typeOptions: {
					maxValue: 100,
					minValue: 0,
				},
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                opportunity:get                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Opportunity ID',
		name: 'opportunityId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['get', 'delete'],
				resource: ['opportunity'],
			},
		},
	},
	/* -------------------------------------------------------------------------- */
	/*                                opportunity:getAll                          */
	/* -------------------------------------------------------------------------- */

	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['opportunity'],
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
		default: 50,
		displayOptions: {
			show: {
				resource: ['opportunity'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		description: 'Max number of results to return',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['getAll', 'get'],
				resource: ['opportunity'],
			},
		},
		options: [
			{
				displayName: 'Fields to Include',
				name: 'fieldsList',
				type: 'multiOptions',
				description:
					'Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: [],
				typeOptions: {
					loadOptionsMethod: 'getModelFields',
				},
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                opportunity:update                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Opportunity ID',
		name: 'opportunityId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['opportunity'],
			},
		},
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['opportunity'],
			},
		},
		options: [
			{
				displayName: 'Email',
				name: 'email_from',
				type: 'string',
				default: '',
			},
			// {
			// 	displayName: 'Expected Closing Date',
			// 	name: 'date_deadline',
			// 	type: 'dateTime',
			// 	default: '',
			// },
			{
				displayName: 'Expected Revenue',
				name: 'expected_revenue',
				type: 'number',
				default: 0,
			},
			{
				displayName: 'Internal Notes',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Phone',
				name: 'phone',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Priority',
				name: 'priority',
				type: 'options',
				default: '1',
				options: [
					{
						name: '1',
						value: '1',
					},
					{
						name: '2',
						value: '2',
					},
					{
						name: '3',
						value: '3',
					},
				],
			},
			{
				displayName: 'Probability',
				name: 'probability',
				type: 'number',
				default: 0,
				typeOptions: {
					maxValue: 100,
					minValue: 0,
				},
			},
		],
	},
];
