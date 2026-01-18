"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Twitter/V1/DirectMessageDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Twitter/V1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:directMessageOperations、directMessageFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Twitter/V1/DirectMessageDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Twitter/V1/DirectMessageDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const directMessageOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['directMessage'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a direct message',
				action: 'Create a direct message',
			},
		],
		default: 'create',
	},
];

export const directMessageFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                directMessage:create                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['directMessage'],
			},
		},
		description: 'The ID of the user who should receive the direct message',
	},
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['directMessage'],
			},
		},
		description:
			'The text of your Direct Message. URL encode as necessary. Max length of 10,000 characters.',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['directMessage'],
			},
		},
		options: [
			{
				displayName: 'Attachment',
				name: 'attachment',
				type: 'string',
				default: 'data',
				description:
					'Name of the binary property which contain data that should be added to the direct message as attachment',
			},
		],
	},
];
