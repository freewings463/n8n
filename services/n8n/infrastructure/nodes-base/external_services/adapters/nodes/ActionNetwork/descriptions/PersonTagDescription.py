"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/descriptions/PersonTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:personTagOperations、personTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/descriptions/PersonTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/descriptions/PersonTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const personTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['personTag'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				action: 'Add a person tag',
			},
			{
				name: 'Remove',
				value: 'remove',
				action: 'Remove a person tag',
			},
		],
		default: 'add',
	},
];

export const personTagFields: INodeProperties[] = [
	// ----------------------------------------
	//             personTag: add
	// ----------------------------------------
	{
		displayName: 'Tag Name or ID',
		name: 'tagId',
		description:
			'ID of the tag to add. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		required: true,
		default: [],
		displayOptions: {
			show: {
				resource: ['personTag'],
				operation: ['add'],
			},
		},
	},
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to add the tag to',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['personTag'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------------
	//             personTag: remove
	// ----------------------------------------
	{
		displayName: 'Tag Name or ID',
		name: 'tagId',
		description:
			'ID of the tag whose tagging to delete. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		default: [],
		required: true,
		displayOptions: {
			show: {
				resource: ['personTag'],
				operation: ['remove'],
			},
		},
	},
	{
		displayName: 'Tagging Name or ID',
		name: 'taggingId',
		description:
			'ID of the tagging to remove. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		typeOptions: {
			loadOptionsDependsOn: ['tagId'],
			loadOptionsMethod: 'getTaggings',
		},
		required: true,
		default: [],
		displayOptions: {
			show: {
				resource: ['personTag'],
				operation: ['remove'],
			},
		},
	},
];
