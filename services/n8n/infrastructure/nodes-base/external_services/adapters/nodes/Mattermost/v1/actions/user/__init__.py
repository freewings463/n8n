"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/user/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create、./deactive、./getAll、./getByEmail 等2项。导出:create、deactive、getAll、getByEmail、getById、invite、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/user/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/user/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create';
import * as deactive from './deactive';
import * as getAll from './getAll';
import * as getByEmail from './getByEmail';
import * as getById from './getById';
import * as invite from './invite';

export { create, deactive, getAll, getByEmail, getById, invite };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['user'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new user',
				action: 'Create a user',
			},
			{
				name: 'Deactive',
				value: 'deactive',
				description:
					'Deactivates the user and revokes all its sessions by archiving its user object',
				action: 'Deactivate a user',
			},
			{
				name: 'Get By Email',
				value: 'getByEmail',
				description: 'Get a user by email',
				action: 'Get a user by email',
			},
			{
				name: 'Get By ID',
				value: 'getById',
				description: 'Get a user by ID',
				action: 'Get a user by ID',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many users',
				action: 'Get many users',
			},
			{
				name: 'Invite',
				value: 'invite',
				description: 'Invite user to team',
				action: 'Invite a user',
			},
		],
		default: '',
	},
	...create.description,
	...deactive.description,
	...getAll.description,
	...getByEmail.description,
	...getById.description,
	...invite.description,
];
