"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Misp/descriptions/OrganisationDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Misp/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:organisationOperations、organisationFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Misp/descriptions/OrganisationDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Misp/descriptions/OrganisationDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const organisationOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['organisation'],
			},
		},
		noDataExpression: true,
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create an organization',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete an organization',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an organization',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many organizations',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update an organization',
			},
		],
		default: 'create',
	},
];

export const organisationFields: INodeProperties[] = [
	// ----------------------------------------
	//           organisation: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Created by Email',
				name: 'created_by_email',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Nationality',
				name: 'nationality',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Sector',
				name: 'sector',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Type',
				name: 'type',
				type: 'string',
				default: '',
			},
			{
				displayName: 'User Count',
				name: 'usercount',
				type: 'number',
				typeOptions: {
					minValue: 0,
				},
				default: 0,
			},
		],
	},

	// ----------------------------------------
	//           organisation: delete
	// ----------------------------------------
	{
		displayName: 'Organisation ID',
		name: 'organisationId',
		description: 'UUID or numeric ID of the organisation',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//            organisation: get
	// ----------------------------------------
	{
		displayName: 'Organisation ID',
		name: 'organisationId',
		description: 'UUID or numeric ID of the organisation',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//           organisation: update
	// ----------------------------------------
	{
		displayName: 'Organisation ID',
		name: 'organisationId',
		description: 'ID of the organisation to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['organisation'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Description',
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
				displayName: 'Nationality',
				name: 'nationality',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Sector',
				name: 'sector',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Type',
				name: 'type',
				type: 'string',
				default: '',
			},
		],
	},
];
