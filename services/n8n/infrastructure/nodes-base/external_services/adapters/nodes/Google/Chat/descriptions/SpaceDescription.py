"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Chat/descriptions/SpaceDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Chat 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../GenericFunctions。导出:spaceOperations、spaceFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Chat/descriptions/SpaceDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Chat/descriptions/SpaceDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { getPagingParameters } from '../GenericFunctions';

export const spaceOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		noDataExpression: true,
		type: 'options',
		displayOptions: {
			show: {
				resource: ['space'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a space',
				action: 'Get a space',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many spaces the caller is a member of',
				action: 'Get many spaces',
			},
		],
		default: 'get',
	},
];

export const spaceFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 space:get                                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Space ID',
		name: 'spaceId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['space'],
				operation: ['get'],
			},
		},
		default: '',
		description: 'Resource name of the space, in the form "spaces/*"',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 space:getAll                               */
	/* -------------------------------------------------------------------------- */

	...getPagingParameters('space'),
];
