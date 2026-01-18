"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Chat/descriptions/MemberDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Chat 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../GenericFunctions。导出:memberOperations、memberFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Chat/descriptions/MemberDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Chat/descriptions/MemberDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { getPagingParameters } from '../GenericFunctions';

export const memberOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		noDataExpression: true,
		type: 'options',
		displayOptions: {
			show: {
				resource: ['member'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a membership',
				action: 'Get a member',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many memberships in a space',
				action: 'Get many members',
			},
		],
		default: 'get',
	},
];

export const memberFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 member:get                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Member ID',
		name: 'memberId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['member'],
				operation: ['get'],
			},
		},
		default: '',
		description: 'Member to be retrieved in the form "spaces/*/members/*"',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 member:getAll                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Space Name or ID',
		name: 'spaceId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getSpaces',
		},
		displayOptions: {
			show: {
				resource: ['member'],
				operation: ['getAll'],
			},
		},
		default: [],
		description:
			'The name of the space for which to retrieve members, in the form "spaces/*". Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},

	...getPagingParameters('member'),
];
