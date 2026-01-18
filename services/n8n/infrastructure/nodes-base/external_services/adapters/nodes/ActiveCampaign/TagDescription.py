"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActiveCampaign/TagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActiveCampaign 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:tagOperations、tagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActiveCampaign/TagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActiveCampaign/TagDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { activeCampaignDefaultGetAllProperties } from './GenericFunctions';

export const tagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['tag'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a tag',
				action: 'Create a tag',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a tag',
				action: 'Delete a tag',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get data of a tag',
				action: 'Get a tag',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get data of many tags',
				action: 'Get many tags',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a tag',
				action: 'Update a tag',
			},
		],
		default: 'create',
	},
];

export const tagFields: INodeProperties[] = [
	// ----------------------------------
	//         contact:create
	// ----------------------------------
	{
		displayName: 'Type',
		name: 'tagType',
		type: 'options',
		default: 'contact',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['tag'],
			},
		},
		options: [
			{
				name: 'Contact',
				value: 'contact',
				description: 'Tag contact',
			},
			{
				name: 'Template',
				value: 'template',
				description: 'Tag template',
			},
		],
		description: 'Tag-type of the new tag',
	},
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['tag'],
			},
		},
		description: 'Name of the new tag',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['tag'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Description of the new tag',
			},
		],
	},
	// ----------------------------------
	//         tag:update
	// ----------------------------------
	{
		displayName: 'Tag ID',
		name: 'tagId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['tag'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the tag to update',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		description: 'The fields to update',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['tag'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Tag',
				name: 'tag',
				type: 'string',
				default: '',
				description: 'Name of the contact',
			},
			{
				displayName: 'Description',
				name: 'description',
				type: 'string',
				default: '',
				description: 'Description of the tag being updated',
			},
		],
	},
	// ----------------------------------
	//         tag:delete
	// ----------------------------------
	{
		displayName: 'Tag ID',
		name: 'tagId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['tag'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the tag to delete',
	},
	// ----------------------------------
	//         contact:get
	// ----------------------------------
	{
		displayName: 'Tag ID',
		name: 'tagId',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['tag'],
			},
		},
		default: 0,
		required: true,
		description: 'ID of the tag to get',
	},
	// ----------------------------------
	//         tag:getAll
	// ----------------------------------
	...activeCampaignDefaultGetAllProperties('tag', 'getAll'),
];
