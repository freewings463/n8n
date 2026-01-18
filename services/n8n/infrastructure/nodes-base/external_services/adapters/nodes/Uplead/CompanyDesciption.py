"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Uplead/CompanyDesciption.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Uplead 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:companyOperations、companyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Uplead/CompanyDesciption.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Uplead/CompanyDesciption.py

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
				name: 'Enrich',
				value: 'enrich',
				action: 'Enrich a company',
			},
		],
		default: 'enrich',
	},
];

export const companyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 company:enrich                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Company',
		name: 'company',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['enrich'],
			},
		},
		description: 'The name of the company (e.g – amazon)',
	},
	{
		displayName: 'Domain',
		name: 'domain',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['company'],
				operation: ['enrich'],
			},
		},
		description: 'The domain name (e.g – amazon.com)',
	},
];
