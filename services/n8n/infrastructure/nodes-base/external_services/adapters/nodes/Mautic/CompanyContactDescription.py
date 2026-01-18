"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mautic/CompanyContactDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mautic 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:companyContactOperations、companyContactFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mautic/CompanyContactDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mautic/CompanyContactDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const companyContactOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['companyContact'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add contact to a company',
				action: 'Add a company contact',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a contact from a company',
				action: 'Remove a company contact',
			},
		],
		default: 'create',
	},
];

export const companyContactFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                companyContact:add                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Contact ID',
		name: 'contactId',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['companyContact'],
				operation: ['add', 'remove'],
			},
		},
		default: '',
		description: 'The ID of the contact',
	},
	{
		displayName: 'Company ID',
		name: 'companyId',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['companyContact'],
				operation: ['add', 'remove'],
			},
		},
		default: '',
		description: 'The ID of the company',
	},
];
