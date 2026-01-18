"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/ticket/update/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:ticketUpdateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/ticket/update/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/ticket/update/description.py

import type { TicketProperties } from '../../Interfaces';

export const ticketUpdateDescription: TicketProperties = [
	{
		displayName: 'Ticket ID',
		name: 'ticketId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['ticket'],
				operation: ['update'],
			},
		},
		default: '',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['ticket'],
				operation: ['update'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Asset ID',
				name: 'assetId',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Assign to Contact',
				name: 'contactId',
				type: 'string',
				default: '',
				description: 'The ID of the contact you want to assign the ticket to',
			},
			{
				displayName: 'Customer ID',
				name: 'customerId',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Due Date',
				name: 'dueDate',
				type: 'dateTime',
				default: '',
			},
			{
				displayName: 'Issue Type',
				name: 'issueType',
				type: 'options',
				options: [
					{
						name: 'Contract Work',
						value: 'Contract Work',
					},
					{
						name: 'Network Project',
						value: 'Network Project',
					},
					{
						name: 'Other',
						value: 'Other',
					},
					{
						name: 'Regular Maintenance',
						value: 'Regular Maintenance',
					},
					{
						name: 'Remote Support',
						value: 'Remote Support',
					},
				],
				default: '',
			},
			{
				displayName: 'Status',
				name: 'status',
				type: 'options',
				options: [
					{
						name: 'Customer Reply',
						value: 'Customer Reply',
					},
					{
						name: 'In Progress',
						value: 'In Progress',
					},
					{
						name: 'New',
						value: 'New',
					},
					{
						name: 'Resolved',
						value: 'Resolved',
					},
					{
						name: 'Scheduled',
						value: 'Scheduled',
					},
					{
						name: 'Waiting for Parts',
						value: 'Waiting for Parts',
					},
					{
						name: 'Waiting on Customer',
						value: 'Waiting on Customer',
					},
				],
				default: 'New',
			},
			{
				displayName: 'Subject',
				name: 'subject',
				type: 'string',
				default: '',
			},
		],
	},
];
