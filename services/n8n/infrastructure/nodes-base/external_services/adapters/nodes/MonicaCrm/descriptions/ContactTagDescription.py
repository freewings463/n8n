"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MonicaCrm/descriptions/ContactTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MonicaCrm/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactTagOperations、contactTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MonicaCrm/descriptions/ContactTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MonicaCrm/descriptions/ContactTagDescription.py

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
				name: 'Add',
				value: 'add',
				action: 'Add a tag to a contact',
			},
			{
				name: 'Remove',
				value: 'remove',
				action: 'Remove a tag from a contact',
			},
		],
		default: 'add',
	},
];

export const contactTagFields: INodeProperties[] = [
	// ----------------------------------------
	//               tag: add
	// ----------------------------------------
	{
		displayName: 'Contact ID',
		name: 'contactId',
		description: 'ID of the contact to add a tag to',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactTag'],
				operation: ['add'],
			},
		},
	},
	{
		displayName: 'Tag Names or IDs',
		name: 'tagsToAdd',
		description:
			'Tags to add to the contact. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'multiOptions',
		typeOptions: {
			loadOptionsMethod: 'getTagsToAdd',
		},
		required: true,
		default: [],
		displayOptions: {
			show: {
				resource: ['contactTag'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------------
	//              tag: remove
	// ----------------------------------------
	{
		displayName: 'Contact ID',
		name: 'contactId',
		description: 'ID of the contact to remove the tag from',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['contactTag'],
				operation: ['remove'],
			},
		},
	},
	{
		displayName: 'Tag Names or IDs',
		name: 'tagsToRemove',
		description:
			'Tags to remove from the contact. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'multiOptions',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getTagsToRemove',
		},
		default: [],
		displayOptions: {
			show: {
				resource: ['contactTag'],
				operation: ['remove'],
			},
		},
	},
];
