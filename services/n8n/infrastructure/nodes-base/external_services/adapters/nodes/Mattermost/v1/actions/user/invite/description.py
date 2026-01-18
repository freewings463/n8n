"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/user/invite/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:userInviteDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/user/invite/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/user/invite/description.py

import type { UserProperties } from '../../Interfaces';

export const userInviteDescription: UserProperties = [
	{
		displayName: 'Team Name or ID',
		name: 'teamId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['invite'],
			},
		},
		default: '',
	},
	{
		displayName: 'Emails',
		name: 'emails',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['user'],
				operation: ['invite'],
			},
		},
		default: '',
		description: "User's email. Multiple emails can be set separated by comma.",
	},
];
