"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBooks/descriptions/Bill/BillAdditionalFieldsOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBooks/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:billAdditionalFieldsOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBooks/descriptions/Bill/BillAdditionalFieldsOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBooks/descriptions/Bill/BillAdditionalFieldsOptions.py

import type { INodeProperties } from 'n8n-workflow';

export const billAdditionalFieldsOptions: INodeProperties[] = [
	{
		displayName: 'Accounts Payable Account',
		name: 'APAccountRef',
		placeholder: 'Add APA Fields',
		description: 'Accounts Payable account to which the bill will be credited',
		type: 'fixedCollection',
		default: {},
		options: [
			{
				displayName: 'Details',
				name: 'details',
				values: [
					{
						displayName: 'Name',
						name: 'name',
						type: 'string',
						default: '',
					},
					{
						displayName: 'ID',
						name: 'value',
						type: 'string',
						default: '',
					},
				],
			},
		],
	},
	{
		displayName: 'Balance',
		name: 'Balance',
		description: 'The balance reflecting any payments made against the transaction',
		type: 'string',
		default: '',
	},
	{
		displayName: 'Due Date',
		name: 'DueDate',
		description: 'Date when the payment of the transaction is due',
		type: 'dateTime',
		default: '',
	},
	{
		displayName: 'Sales Term',
		name: 'SalesTermRef',
		description: 'Sales term associated with the transaction',
		placeholder: 'Add Sales Term Fields',
		type: 'fixedCollection',
		default: {},
		options: [
			{
				displayName: 'Details',
				name: 'details',
				values: [
					{
						displayName: 'Name',
						name: 'name',
						type: 'string',
						default: '',
					},
					{
						displayName: 'ID',
						name: 'value',
						type: 'string',
						default: '',
					},
				],
			},
		],
	},
	{
		displayName: 'Total Amount',
		name: 'TotalAmt',
		description: 'Total amount of the transaction',
		type: 'number',
		default: 0,
	},
	{
		displayName: 'Transaction Date',
		name: 'TxnDate',
		description: 'Date when the transaction occurred',
		type: 'dateTime',
		default: '',
	},
];
