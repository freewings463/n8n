"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clearbit/PersonDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clearbit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:personOperations、personFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clearbit/PersonDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clearbit/PersonDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const personOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['person'],
			},
		},
		options: [
			{
				name: 'Enrich',
				value: 'enrich',
				description: 'Look up a person and company data based on an email or domain',
				action: 'Enrich a person',
			},
		],
		default: 'enrich',
	},
];

export const personFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 person:enrich                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['enrich'],
			},
		},
		description: 'The email address to look up',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['enrich'],
			},
		},
		options: [
			{
				displayName: 'Company',
				name: 'company',
				type: 'string',
				default: '',
				description: 'The name of the person’s employer',
			},
			{
				displayName: 'Company Domain',
				name: 'companyDomain',
				type: 'string',
				default: '',
				description: 'The domain for the person’s employer',
			},
			{
				displayName: 'Facebook',
				name: 'facebook',
				type: 'string',
				default: '',
				description: 'The Facebook URL for the person',
			},
			{
				displayName: 'Family Name',
				name: 'familyName',
				type: 'string',
				default: '',
				description:
					'Last name of person. If you have this, passing this is strongly recommended to improve match rates.',
			},
			{
				displayName: 'Given Name',
				name: 'givenName',
				type: 'string',
				default: '',
				description: 'First name of person',
			},
			{
				displayName: 'IP Address',
				name: 'ipAddress',
				type: 'string',
				default: '',
				description:
					'IP address of the person. If you have this, passing this is strongly recommended to improve match rates.',
			},
			{
				displayName: 'Location',
				name: 'location',
				type: 'string',
				default: '',
				description: 'The city or country where the person resides',
			},
			{
				displayName: 'LinkedIn',
				name: 'linkedIn',
				type: 'string',
				default: '',
				description: 'The LinkedIn URL for the person',
			},
			{
				displayName: 'Twitter',
				name: 'twitter',
				type: 'string',
				default: '',
				description: 'The Twitter handle for the person',
			},
		],
	},
];
