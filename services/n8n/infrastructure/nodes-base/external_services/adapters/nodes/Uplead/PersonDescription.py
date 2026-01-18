"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Uplead/PersonDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Uplead 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:personOperations、personFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Uplead/PersonDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Uplead/PersonDescription.py

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
				action: 'Enrich a person',
			},
		],
		default: 'enrich',
	},
];

export const personFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 person:enrich                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['enrich'],
			},
		},
		description: 'Email address (e.g – mbenioff@salesforce.com)',
	},
	{
		displayName: 'First Name',
		name: 'firstname',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['enrich'],
			},
		},
		description: 'First name of the person (e.g – Marc)',
	},
	{
		displayName: 'Last Name',
		name: 'lastname',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['enrich'],
			},
		},
		description: 'Last name of the person (e.g – Benioff)',
	},
	{
		displayName: 'Domain',
		name: 'domain',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['person'],
				operation: ['enrich'],
			},
		},
		description: 'The domain name (e.g – salesforce.com)',
	},
];
