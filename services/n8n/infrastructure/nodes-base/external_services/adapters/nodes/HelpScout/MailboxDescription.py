"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HelpScout/MailboxDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HelpScout 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:mailboxOperations、mailboxFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HelpScout/MailboxDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HelpScout/MailboxDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const mailboxOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['mailbox'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get data of a mailbox',
				action: 'Get a mailbox',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many mailboxes',
				action: 'Get many mailboxes',
			},
		],
		default: 'get',
	},
];

export const mailboxFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                mailbox:get                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Mailbox ID',
		name: 'mailboxId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['mailbox'],
				operation: ['get'],
			},
		},
	},
	/* -------------------------------------------------------------------------- */
	/*                                mailbox:getAll                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['mailbox'],
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
				resource: ['mailbox'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
		},
		default: 50,
		description: 'Max number of results to return',
	},
];
