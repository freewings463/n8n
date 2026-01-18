"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/reaction/getAll/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:reactionGetAllDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/reaction/getAll/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/reaction/getAll/description.py

import type { ReactionProperties } from '../../Interfaces';

export const reactionGetAllDescription: ReactionProperties = [
	{
		displayName: 'Post ID',
		name: 'postId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['reaction'],
				operation: ['getAll'],
			},
		},
		description: 'One or more (comma-separated) posts to retrieve reactions from',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['reaction'],
			},
		},
		default: true,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['reaction'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
