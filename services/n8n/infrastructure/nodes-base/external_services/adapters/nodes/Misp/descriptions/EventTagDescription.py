"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Misp/descriptions/EventTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Misp/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventTagOperations、eventTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Misp/descriptions/EventTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Misp/descriptions/EventTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const eventTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['eventTag'],
			},
		},
		noDataExpression: true,
		options: [
			{
				name: 'Add',
				value: 'add',
				action: 'Add a tag to an event',
			},
			{
				name: 'Remove',
				value: 'remove',
				action: 'Remove a tag from an event',
			},
		],
		default: 'add',
	},
];

export const eventTagFields: INodeProperties[] = [
	// ----------------------------------------
	//             eventTag: add
	// ----------------------------------------
	{
		displayName: 'Event ID',
		name: 'eventId',
		description: 'UUID or numeric ID of the event',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['eventTag'],
				operation: ['add'],
			},
		},
	},
	{
		displayName: 'Tag Name or ID',
		name: 'tagId',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		displayOptions: {
			show: {
				resource: ['eventTag'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------------
	//            eventTag: remove
	// ----------------------------------------
	{
		displayName: 'Event ID',
		name: 'eventId',
		description: 'UUID or numeric ID of the event',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['eventTag'],
				operation: ['remove'],
			},
		},
	},
	{
		displayName: 'Tag Name or ID',
		name: 'tagId',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		displayOptions: {
			show: {
				resource: ['eventTag'],
				operation: ['remove'],
			},
		},
	},
];
