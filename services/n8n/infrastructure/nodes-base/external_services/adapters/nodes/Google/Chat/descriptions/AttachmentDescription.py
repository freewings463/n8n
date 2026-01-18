"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Chat/descriptions/AttachmentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Chat 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:attachmentOperations、attachmentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Chat/descriptions/AttachmentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Chat/descriptions/AttachmentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const attachmentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		noDataExpression: true,
		type: 'options',
		displayOptions: {
			show: {
				resource: ['attachment'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description:
					'Gets the metadata of a message attachment. The attachment data is fetched using the media API.',
				action: 'Get an attachment',
			},
		],
		default: 'get',
	},
];

export const attachmentFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 attachments:get                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Attachment Name',
		name: 'attachmentName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['attachment'],
				operation: ['get'],
			},
		},
		default: '',
		description: 'Resource name of the attachment, in the form "spaces/*/messages/*/attachments/*"',
	},
];
