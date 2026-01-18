"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/customer/update/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:无；本地:../methods/sharedFields、../../Interfaces。导出:customerUpdateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/customer/update/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/customer/update/description.py

import { addressFixedCollection } from '../../../methods/sharedFields';
import type { CustomerProperties } from '../../Interfaces';

export const customerUpdateDescription: CustomerProperties = [
	{
		displayName: 'Customer ID',
		name: 'customerId',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['customer'],
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
				resource: ['customer'],
				operation: ['update'],
			},
		},
		default: {},
		options: [
			addressFixedCollection,
			{
				displayName: 'Business Name',
				name: 'businessName',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
			},
			{
				displayName: 'First Name',
				name: 'firstName',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Get SMS',
				name: 'getSms',
				type: 'boolean',
				default: true,
			},
			{
				displayName: 'Invoice Emails',
				name: 'invoiceCcEmails',
				type: 'string',
				typeOptions: {
					multipleValues: true,
					multipleValueButtonText: 'Add Email',
				},
				default: '',
			},
			{
				displayName: 'Last Name',
				name: 'lastName',
				type: 'string',
				default: '',
			},
			{
				displayName: 'No Email',
				name: 'noEmail',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Notes',
				name: 'notes',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Notification Email',
				name: 'notificationEmail',
				type: 'string',
				default: '',
				displayOptions: {
					show: {
						noEmail: [false],
					},
				},
			},
			{
				displayName: 'Phone',
				name: 'phone',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Referred By',
				name: 'referredBy',
				type: 'string',
				default: '',
				description:
					'Source from which customer is referred to the platform like Linkedin, Google, Customer name etc',
			},
		],
	},
];
