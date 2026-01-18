"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Trello/CardCommentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Trello 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:cardCommentOperations、cardCommentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Trello/CardCommentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Trello/CardCommentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const cardCommentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['cardComment'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a comment on a card',
				action: 'Create a card comment',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a comment from a card',
				action: 'Delete a card comment',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a comment on a card',
				action: 'Update a card comment',
			},
		],
		default: 'create',
	},
];

export const cardCommentFields: INodeProperties[] = [
	{
		displayName: 'Card',
		name: 'cardId',
		type: 'resourceLocator',
		default: { mode: 'list', value: '' },
		required: true,
		modes: [
			{
				displayName: 'From List',
				name: 'list',
				type: 'list',
				placeholder: 'Select a Card...',
				typeOptions: {
					searchListMethod: 'searchCards',
					searchFilterRequired: true,
					searchable: true,
				},
			},
			{
				displayName: 'By URL',
				name: 'url',
				type: 'string',
				placeholder: 'https://trello.com/c/e123456/card-name',
				validation: [
					{
						type: 'regex',
						properties: {
							regex: 'http(s)?://trello.com/c/([a-zA-Z0-9]{2,})/.*',
							errorMessage: 'Not a valid Trello Card URL',
						},
					},
				],
				extractValue: {
					type: 'regex',
					regex: 'https://trello.com/c/([a-zA-Z0-9]{2,})',
				},
			},
			{
				displayName: 'ID',
				name: 'id',
				type: 'string',
				validation: [
					{
						type: 'regex',
						properties: {
							regex: '[a-zA-Z0-9]{2,}',
							errorMessage: 'Not a valid Trello Card ID',
						},
					},
				],
				placeholder: 'wiIaGwqE',
				url: '=https://trello.com/c/{{$value}}',
			},
		],
		displayOptions: {
			show: {
				operation: ['update', 'delete', 'create'],
				resource: ['cardComment'],
			},
		},
		description: 'The ID of the card',
	},

	// ----------------------------------
	//         cardComment:create
	// ----------------------------------
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['cardComment'],
			},
		},
		description: 'Text of the comment',
	},

	// ----------------------------------
	//         cardComment:remove
	// ----------------------------------
	{
		displayName: 'Comment ID',
		name: 'commentId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete'],
				resource: ['cardComment'],
			},
		},
		description: 'The ID of the comment to delete',
	},

	// ----------------------------------
	//         cardComment:update
	// ----------------------------------
	{
		displayName: 'Comment ID',
		name: 'commentId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['cardComment'],
			},
		},
		description: 'The ID of the comment to delete',
	},
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['cardComment'],
			},
		},
		description: 'Text of the comment',
	},
];
