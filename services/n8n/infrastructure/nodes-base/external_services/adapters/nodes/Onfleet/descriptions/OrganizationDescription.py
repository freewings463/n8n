"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Onfleet/descriptions/OrganizationDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Onfleet/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:organizationOperations、organizationFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Onfleet/descriptions/OrganizationDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Onfleet/descriptions/OrganizationDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const organizationOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['organization'],
			},
		},
		options: [
			{
				name: 'Get My Organization',
				value: 'get',
				description: "Retrieve your own organization's details",
				action: 'Get my organization',
			},
			{
				name: 'Get Delegatee Details',
				value: 'getDelegatee',
				description: 'Retrieve the details of an organization with which you are connected',
				action: "Get a delegatee's details",
			},
		],
		default: 'get',
	},
];

export const organizationFields: INodeProperties[] = [
	{
		displayName: 'Organization ID',
		name: 'id',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['organization'],
				operation: ['getDelegatee'],
			},
		},
		default: '',
		required: true,
		description: 'The ID of the delegatees for lookup',
	},
];
