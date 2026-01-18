"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/descriptions/PersonDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./SharedFields。导出:personOperations、personFields。关键函数/方法:makeSimpleField。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/descriptions/PersonDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/descriptions/PersonDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { makeSimpleField, personAdditionalFieldsOptions } from './SharedFields';

export const personOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['person'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a person',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a person',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many people',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a person',
			},
		],
		default: 'create',
	},
];

export const personFields: INodeProperties[] = [
	// ----------------------------------------
	//              person: create
	// ----------------------------------------
	makeSimpleField('person', 'create'),
	{
		displayName: 'Email Address', // on create, only _one_ must be passed in
		name: 'email_addresses',
		type: 'fixedCollection',
		default: {},
		placeholder: 'Add Email Address Field',
		description: 'Person’s email addresses',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Email Addresses Fields',
				name: 'email_addresses_fields',
				values: [
					{
						displayName: 'Address',
						name: 'address',
						type: 'string',
						default: '',
						description: "Person's email address",
					},
					{
						displayName: 'Primary',
						name: 'primary',
						type: 'hidden',
						default: true,
						description: "Whether this is the person's primary email address",
					},
					{
						displayName: 'Status',
						name: 'status',
						type: 'options',
						default: 'subscribed',
						description: 'Subscription status of this email address',
						options: [
							{
								name: 'Bouncing',
								value: 'bouncing',
							},
							{
								name: 'Previous Bounce',
								value: 'previous bounce',
							},
							{
								name: 'Previous Spam Complaint',
								value: 'previous spam complaint',
							},
							{
								name: 'Spam Complaint',
								value: 'spam complaint',
							},
							{
								name: 'Subscribed',
								value: 'subscribed',
							},
							{
								name: 'Unsubscribed',
								value: 'unsubscribed',
							},
						],
					},
				],
			},
		],
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['create'],
			},
		},
		options: personAdditionalFieldsOptions,
	},

	// ----------------------------------------
	//               person: get
	// ----------------------------------------
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['get'],
			},
		},
	},
	makeSimpleField('person', 'get'),

	// ----------------------------------------
	//              person: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 25,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 25,
		},
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	makeSimpleField('person', 'getAll'),

	// ----------------------------------------
	//              person: update
	// ----------------------------------------
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['update'],
			},
		},
	},
	makeSimpleField('person', 'update'),
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['update'],
			},
		},
		options: personAdditionalFieldsOptions,
	},
];
