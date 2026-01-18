"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SecurityScorecard/descriptions/InviteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SecurityScorecard/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:inviteOperations、inviteFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SecurityScorecard/descriptions/InviteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SecurityScorecard/descriptions/InviteDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const inviteOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		displayOptions: {
			show: {
				resource: ['invite'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an invite for a company/user',
				action: 'Create an invite',
			},
		],
		default: 'create',
	},
];

export const inviteFields: INodeProperties[] = [
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['invite'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'First Name',
		name: 'firstName',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['invite'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Last Name',
		name: 'lastName',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['invite'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Message',
		name: 'message',
		description: 'Message for the invitee',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['invite'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['invite'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Days to Resolve Issue',
				description: 'Minimum days to resolve a scorecard issue',
				name: 'days_to_resolve_issue',
				type: 'number',
				default: 0,
			},
			{
				displayName: 'Domain',
				description: 'Invitee company domain',
				name: 'domain',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Grade to Maintain',
				description: "Request the invitee's organisation to maintain a minimum grade",
				name: 'grade_to_maintain',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Is Organisation Point of Contact',
				// eslint-disable-next-line n8n-nodes-base/node-param-description-boolean-without-whether
				description: "Is the invitee organisation's point of contact",
				name: 'is_organization_point_of_contact',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Issue Description',
				name: 'issue_desc',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Issue Title',
				name: 'issue_title',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Issue Type',
				name: 'issue_type',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Send Me a Copy',
				name: 'sendme_copy',
				description: 'Whether to send a copy of the invite to the requesting user',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Target URL',
				name: 'target_url',
				type: 'string',
				description: 'Optional URL to take the invitee to when arriving to the platform',
				default: '',
			},
		],
	},
];
