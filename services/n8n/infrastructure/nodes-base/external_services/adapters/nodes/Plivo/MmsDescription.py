"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Plivo/MmsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Plivo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:mmsOperations、mmsFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Plivo/MmsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Plivo/MmsDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const mmsOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['mms'],
			},
		},
		options: [
			{
				name: 'Send',
				value: 'send',
				description: 'Send an MMS message (US/Canada only)',
				action: 'Send an MMS',
			},
		],
		default: 'send',
	},
];

export const mmsFields: INodeProperties[] = [
	// ----------------------------------
	//           mms: send
	// ----------------------------------
	{
		displayName: 'From',
		name: 'from',
		type: 'string',
		default: '',
		description: 'Plivo Number to send the MMS from',
		placeholder: '+14156667777',
		required: true,
		displayOptions: {
			show: {
				resource: ['mms'],
				operation: ['send'],
			},
		},
	},
	{
		displayName: 'To',
		name: 'to',
		type: 'string',
		default: '',
		description: 'Phone number to send the MMS to',
		placeholder: '+14156667778',
		required: true,
		displayOptions: {
			show: {
				operation: ['send'],
				resource: ['mms'],
			},
		},
	},
	{
		displayName: 'Message',
		name: 'message',
		type: 'string',
		default: '',
		description: 'Message to send',
		displayOptions: {
			show: {
				resource: ['mms'],
				operation: ['send'],
			},
		},
	},
	{
		displayName: 'Media URLs',
		name: 'media_urls',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['mms'],
				operation: ['send'],
			},
		},
		description: 'Comma-separated list of media URLs of the files from your file server',
	},
];
