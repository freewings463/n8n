"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zendesk/TicketFieldDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zendesk 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ticketFieldOperations、ticketFieldFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zendesk/TicketFieldDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zendesk/TicketFieldDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const ticketFieldOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['ticketField'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a ticket field',
				action: 'Get a ticket field',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many system and custom ticket fields',
				action: 'Get many ticket fields',
			},
		],
		default: 'get',
	},
];

export const ticketFieldFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 ticketField:get                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Ticket Field ID',
		name: 'ticketFieldId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['ticketField'],
				operation: ['get'],
			},
		},
	},

	/* -------------------------------------------------------------------------- */
	/*                                 ticketField:getAll                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['ticketField'],
				operation: ['getAll'],
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
				resource: ['ticketField'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
