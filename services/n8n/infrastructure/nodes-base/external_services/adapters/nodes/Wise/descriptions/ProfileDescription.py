"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wise/descriptions/ProfileDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wise/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:profileOperations、profileFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wise/descriptions/ProfileDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wise/descriptions/ProfileDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const profileOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get a profile',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many profiles',
			},
		],
		displayOptions: {
			show: {
				resource: ['profile'],
			},
		},
	},
];

export const profileFields: INodeProperties[] = [
	// ----------------------------------
	//         profile: get
	// ----------------------------------
	{
		displayName: 'Profile Name or ID',
		name: 'profileId',
		type: 'options',
		required: true,
		default: [],
		typeOptions: {
			loadOptionsMethod: 'getProfiles',
		},
		description:
			'ID of the user profile to retrieve. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		displayOptions: {
			show: {
				resource: ['profile'],
				operation: ['get'],
			},
		},
	},
];
