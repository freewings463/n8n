"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Plivo/SmsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Plivo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:smsOperations、smsFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Plivo/SmsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Plivo/SmsDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const smsOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['sms'],
			},
		},
		options: [
			{
				name: 'Send',
				value: 'send',
				description: 'Send an SMS message',
				action: 'Send an SMS',
			},
		],
		default: 'send',
	},
];

export const smsFields: INodeProperties[] = [
	// ----------------------------------
	//           sms: send
	// ----------------------------------
	{
		displayName: 'From',
		name: 'from',
		type: 'string',
		default: '',
		description: 'Plivo Number to send the SMS from',
		placeholder: '+14156667777',
		required: true,
		displayOptions: {
			show: {
				resource: ['sms'],
				operation: ['send'],
			},
		},
	},
	{
		displayName: 'To',
		name: 'to',
		type: 'string',
		default: '',
		description: 'Phone number to send the message to',
		placeholder: '+14156667778',
		required: true,
		displayOptions: {
			show: {
				resource: ['sms'],
				operation: ['send'],
			},
		},
	},
	{
		displayName: 'Message',
		name: 'message',
		type: 'string',
		default: '',
		description: 'Message to send',
		required: true,
		displayOptions: {
			show: {
				operation: ['send'],
				resource: ['sms'],
			},
		},
	},
];
