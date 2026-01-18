"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Gmail/v1/MessageLabelDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Gmail 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:messageLabelOperations、messageLabelFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Gmail/v1/MessageLabelDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Gmail/v1/MessageLabelDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const messageLabelOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['messageLabel'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				action: 'Add a label to a message',
			},
			{
				name: 'Remove',
				value: 'remove',
				action: 'Remove a label from a message',
			},
		],
		default: 'add',
	},
];

export const messageLabelFields: INodeProperties[] = [
	{
		displayName: 'Message ID',
		name: 'messageId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['messageLabel'],
				operation: ['add', 'remove'],
			},
		},
		placeholder: '172ce2c4a72cc243',
	},
	{
		displayName: 'Label Names or IDs',
		name: 'labelIds',
		type: 'multiOptions',
		typeOptions: {
			loadOptionsMethod: 'getLabels',
		},
		default: [],
		required: true,
		displayOptions: {
			show: {
				resource: ['messageLabel'],
				operation: ['add', 'remove'],
			},
		},
		description:
			'The ID of the label. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
];
