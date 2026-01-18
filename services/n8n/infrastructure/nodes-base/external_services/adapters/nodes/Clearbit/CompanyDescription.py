"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clearbit/CompanyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clearbit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:companyOperations、companyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clearbit/CompanyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clearbit/CompanyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const companyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['company'],
			},
		},
		options: [
			{
				name: 'Autocomplete',
				value: 'autocomplete',
				description: 'Auto-complete company names and retrieve logo and domain',
				action: 'Autocomplete a company',
			},
			{
				name: 'Enrich',
				value: 'enrich',
				description: 'Look up person and company data based on an email or domain',
				action: 'Enrich a company',
			},
		],
		default: 'enrich',
	},
];

export const companyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 company:enrich                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Domain',
		name: 'domain',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['enrich'],
			},
		},
		description: 'The domain to look up',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['enrich'],
			},
		},
		options: [
			{
				displayName: 'Company Name',
				name: 'companyName',
				type: 'string',
				default: '',
				description: 'The name of the company',
			},
			{
				displayName: 'Facebook',
				name: 'facebook',
				type: 'string',
				default: '',
				description: 'The Facebook URL for the company',
			},
			{
				displayName: 'Linkedin',
				name: 'linkedin',
				type: 'string',
				default: '',
				description: 'The LinkedIn URL for the company',
			},
			{
				displayName: 'Twitter',
				name: 'twitter',
				type: 'string',
				default: '',
				description: 'The Twitter handle for the company',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                 company:autocomplete                       */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['autocomplete'],
			},
		},
		description: 'Name is the partial name of the company',
	},
];
