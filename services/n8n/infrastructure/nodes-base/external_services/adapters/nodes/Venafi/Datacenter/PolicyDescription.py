"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Venafi/Datacenter/PolicyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Venafi/Datacenter 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:policyOperations、policyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Venafi/Datacenter/PolicyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Venafi/Datacenter/PolicyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const policyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['policy'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a policy',
				action: 'Get a policy',
			},
		],
		default: 'get',
	},
];

export const policyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 policy:get                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Policy DN',
		name: 'policyDn',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['policy'],
			},
		},
		default: '',
		description: 'The Distinguished Name (DN) of the policy folder',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['policy'],
			},
		},
		options: [
			{
				displayName: 'PKCS10',
				name: 'PKCS10',
				type: 'string',
				default: '',
				description:
					'The PKCS#10 policy Signing Request (CSR). Omit escape characters such as or . If this value is provided, any Subject DN fields and the KeyBitSize in the request are ignored.',
			},
		],
	},
];
