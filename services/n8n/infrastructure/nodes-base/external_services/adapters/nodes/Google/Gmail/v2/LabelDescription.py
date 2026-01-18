"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Gmail/v2/LabelDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Gmail 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:labelOperations、labelFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Gmail/v2/LabelDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Gmail/v2/LabelDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const labelOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['label'],
			},
		},

		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a label',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a label',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a label info',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many labels',
			},
		],
		default: 'getAll',
	},
];

export const labelFields: INodeProperties[] = [
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['label'],
				operation: ['create'],
			},
		},
		placeholder: 'invoices',
		description: 'Label Name',
	},
	{
		displayName: 'Label ID',
		name: 'labelId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['label'],
				operation: ['get', 'delete'],
			},
		},
		description: 'The ID of the label',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		displayOptions: {
			show: {
				resource: ['label'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Label List Visibility',
				name: 'labelListVisibility',
				type: 'options',
				options: [
					{
						name: 'Hide',
						value: 'labelHide',
					},
					{
						name: 'Show',
						value: 'labelShow',
					},
					{
						name: 'Show If Unread',
						value: 'labelShowIfUnread',
					},
				],
				default: 'labelShow',
				description: 'The visibility of the label in the label list in the Gmail web interface',
			},
			{
				displayName: 'Message List Visibility',
				name: 'messageListVisibility',
				type: 'options',
				options: [
					{
						name: 'Hide',
						value: 'hide',
					},
					{
						name: 'Show',
						value: 'show',
					},
				],
				default: 'show',
				description:
					'The visibility of messages with this label in the message list in the Gmail web interface',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                 label:getAll                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['label'],
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
				resource: ['label'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 50,
		description: 'Max number of results to return',
	},
];
