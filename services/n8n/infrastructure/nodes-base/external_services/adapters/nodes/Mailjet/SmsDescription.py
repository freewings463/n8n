"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mailjet/SmsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mailjet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:smsOperations、smsFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mailjet/SmsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mailjet/SmsDescription.py

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
				description: 'Send a sms',
				action: 'Send an SMS',
			},
		],
		default: 'send',
	},
];

export const smsFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                sms:send                                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'From',
		name: 'from',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['sms'],
				operation: ['send'],
			},
		},
		description:
			'Customizable sender name. Should be between 3 and 11 characters in length, only alphanumeric characters are allowed.',
	},
	{
		displayName: 'To',
		name: 'to',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['sms'],
				operation: ['send'],
			},
		},
		description:
			'Message recipient. Should be between 3 and 15 characters in length. The number always starts with a plus sign followed by a country code, followed by the number. Phone numbers are expected to comply with the E.164 format.',
	},
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['sms'],
				operation: ['send'],
			},
		},
	},
];
