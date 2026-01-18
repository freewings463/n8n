"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/descriptions/common.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils。导出:paginationParameters、userLocator、groupLocator、pathParameter、groupNameParameter、userNameParameter。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/descriptions/common.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/descriptions/common.py

import type { INodeProperties } from 'n8n-workflow';

import { validateName } from '../helpers/utils';

export const paginationParameters: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		default: 100,
		type: 'number',
		validateType: 'number',
		typeOptions: {
			minValue: 1,
		},
		description: 'Max number of results to return',
		displayOptions: {
			hide: {
				returnAll: [true],
			},
		},
		routing: {
			send: {
				property: 'MaxItems',
				type: 'body',
				value: '={{ $value }}',
			},
		},
	},
];

export const userLocator: INodeProperties = {
	displayName: 'User',
	name: 'user',
	required: true,
	type: 'resourceLocator',
	default: {
		mode: 'list',
		value: '',
	},
	modes: [
		{
			displayName: 'From list',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchUsers',
				searchable: true,
			},
		},
		{
			displayName: 'By Name',
			name: 'userName',
			type: 'string',
			placeholder: 'e.g. Admins',
			hint: 'Enter the user name',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '^[\\w+=,.@-]+$',
						errorMessage: 'The user name must follow the allowed pattern',
					},
				},
			],
		},
	],
};

export const groupLocator: INodeProperties = {
	displayName: 'Group',
	name: 'group',
	required: true,
	type: 'resourceLocator',
	default: {
		mode: 'list',
		value: '',
	},
	modes: [
		{
			displayName: 'From list',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchGroups',
				searchable: true,
			},
		},
		{
			displayName: 'By Name',
			name: 'groupName',
			type: 'string',
			placeholder: 'e.g. Admins',
			hint: 'Enter the group name',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '^[\\w+=,.@-]+$',
						errorMessage: 'The group name must follow the allowed pattern.',
					},
				},
			],
		},
	],
};

export const pathParameter: INodeProperties = {
	displayName: 'Path',
	name: 'path',
	type: 'string',
	validateType: 'string',
	default: '/',
};

export const groupNameParameter: INodeProperties = {
	displayName: 'Group Name',
	name: 'groupName',
	required: true,
	type: 'string',
	validateType: 'string',
	typeOptions: {
		maxLength: 128,
		regex: '^[+=,.@\\-_A-Za-z0-9]+$',
	},
	default: '',
	placeholder: 'e.g. GroupName',
	routing: {
		send: {
			preSend: [validateName],
		},
	},
};

export const userNameParameter: INodeProperties = {
	displayName: 'User Name',
	name: 'userName',
	required: true,
	type: 'string',
	validateType: 'string',
	default: '',
	placeholder: 'e.g. JohnSmith',
	typeOptions: {
		maxLength: 64,
		regex: '^[A-Za-z0-9+=,\\.@_-]+$',
	},
	routing: {
		send: {
			preSend: [validateName],
		},
	},
};
