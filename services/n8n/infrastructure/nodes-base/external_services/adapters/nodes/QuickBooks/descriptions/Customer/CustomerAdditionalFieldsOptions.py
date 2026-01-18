"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBooks/descriptions/Customer/CustomerAdditionalFieldsOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBooks/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:customerAdditionalFieldsOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBooks/descriptions/Customer/CustomerAdditionalFieldsOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBooks/descriptions/Customer/CustomerAdditionalFieldsOptions.py

import type { INodeProperties } from 'n8n-workflow';

export const customerAdditionalFieldsOptions: INodeProperties[] = [
	{
		displayName: 'Active',
		name: 'Active',
		description: 'Whether the customer is currently enabled for use by QuickBooks',
		type: 'boolean',
		default: true,
	},
	{
		displayName: 'Balance',
		name: 'Balance',
		description: 'Open balance amount or amount unpaid by the customer',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Balance With Jobs',
		name: 'BalanceWithJobs',
		description: 'Cumulative open balance amount for the customer (or job) and all its sub-jobs',
		type: 'number',
		default: 0,
	},
	{
		displayName: 'Billing Address',
		name: 'BillAddr',
		placeholder: 'Add Billing Address Fields',
		type: 'fixedCollection',
		default: {},
		options: [
			{
				displayName: 'Details',
				name: 'details',
				values: [
					{
						displayName: 'City',
						name: 'City',
						type: 'string',
						default: '',
					},
					{
						displayName: 'Line 1',
						name: 'Line1',
						type: 'string',
						default: '',
					},
					{
						displayName: 'Postal Code',
						name: 'PostalCode',
						type: 'string',
						default: '',
					},
					{
						displayName: 'Latitude',
						name: 'Lat',
						type: 'string',
						default: '',
					},
					{
						displayName: 'Longitude',
						name: 'Long',
						type: 'string',
						default: '',
					},
					{
						displayName: 'Country Subdivision Code',
						name: 'CountrySubDivisionCode',
						type: 'string',
						default: '',
					},
				],
			},
		],
	},
	{
		displayName: 'Bill With Parent',
		name: 'BillWithParent',
		description: 'Whether to bill this customer together with its parent',
		type: 'boolean',
		default: false,
	},
	{
		displayName: 'Company Name',
		name: 'CompanyName',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Family Name',
		name: 'FamilyName',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Fully Qualified Name',
		name: 'FullyQualifiedName',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Given Name',
		name: 'GivenName',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Preferred Delivery Method',
		name: 'PreferredDeliveryMethod',
		type: 'options',
		default: 'Print',
		options: [
			{
				name: 'Print',
				value: 'Print',
			},
			{
				name: 'Email',
				value: 'Email',
			},
			{
				name: 'None',
				value: 'None',
			},
		],
	},
	{
		displayName: 'Primary Email Address',
		name: 'PrimaryEmailAddr',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Primary Phone',
		name: 'PrimaryPhone',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Print-On-Check Name',
		name: 'PrintOnCheckName',
		description: 'Name of the customer as printed on a check',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Taxable',
		name: 'Taxable',
		description: 'Whether transactions for this customer are taxable',
		type: 'boolean',
		default: false,
	},
];
