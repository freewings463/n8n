"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshservice/descriptions/RequesterGroupDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshservice/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:requesterGroupOperations、requesterGroupFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshservice/descriptions/RequesterGroupDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshservice/descriptions/RequesterGroupDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const requesterGroupOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['requesterGroup'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a requester group',
				action: 'Create a requester group',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a requester group',
				action: 'Delete a requester group',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a requester group',
				action: 'Get a requester group',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many requester groups',
				action: 'Get many requester groups',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a requester group',
				action: 'Update a requester group',
			},
		],
		default: 'create',
	},
];

export const requesterGroupFields: INodeProperties[] = [
	// ----------------------------------------
	//          requesterGroup: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requesterGroup'],
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
				resource: ['requesterGroup'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
			},
		],
	},

	// ----------------------------------------
	//          requesterGroup: delete
	// ----------------------------------------
	{
		displayName: 'Requester Group ID',
		name: 'requesterGroupId',
		description: 'ID of the requester group to delete',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requesterGroup'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//           requesterGroup: get
	// ----------------------------------------
	{
		displayName: 'Requester Group ID',
		name: 'requesterGroupId',
		description: 'ID of the requester group to retrieve',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requesterGroup'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//          requesterGroup: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['requesterGroup'],
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
				resource: ['requesterGroup'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},

	// ----------------------------------------
	//          requesterGroup: update
	// ----------------------------------------
	{
		displayName: 'Requester Group ID',
		name: 'requesterGroupId',
		description: 'ID of the requester group to update',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['requesterGroup'],
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
				resource: ['requesterGroup'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Description of the requester group',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'Name of the requester group',
			},
		],
	},
];
