"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Linear/CommentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Linear 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:commentOperations、commentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Linear/CommentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Linear/CommentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const commentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['comment'],
			},
		},
		options: [
			{
				name: 'Add Comment',
				value: 'addComment',
				description: 'Add a comment to an issue',
				action: 'Add a comment to an issue',
			},
		],
		default: 'addComment',
	},
];

export const commentFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                comment:addComment                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Issue ID',
		name: 'issueId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['comment'],
				operation: ['addComment'],
			},
		},
		default: '',
	},
	{
		displayName: 'Comment',
		name: 'comment',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['comment'],
				operation: ['addComment'],
			},
		},
		default: '',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['comment'],
				operation: ['addComment'],
			},
		},
		options: [
			{
				displayName: 'Parent Comment ID',
				name: 'parentId',
				type: 'string',
				description: 'ID of the parent comment if this is a reply',
				default: '',
			},
		],
	},
];
