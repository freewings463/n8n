"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/descriptions/user/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/descriptions/user/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/descriptions/user/create_operation.py

import type { INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { preprocessTags, validatePath, validatePermissionsBoundary } from '../../helpers/utils';
import { pathParameter, userNameParameter } from '../common';

const properties: INodeProperties[] = [
	{
		...userNameParameter,
		description: 'The username of the new user to create',
		placeholder: 'e.g. UserName',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [
			{
				...pathParameter,
				description: 'The path for the user name',
				placeholder: 'e.g. /division_abc/subdivision_xyz/',
				routing: {
					send: {
						preSend: [validatePath],
						property: 'Path',
						type: 'query',
					},
				},
			},
			{
				displayName: 'Permissions Boundary',
				name: 'permissionsBoundary',
				default: '',
				description:
					'The ARN of the managed policy that is used to set the permissions boundary for the user',
				placeholder: 'e.g. arn:aws:iam::123456789012:policy/ExampleBoundaryPolicy',
				type: 'string',
				validateType: 'string',
				routing: {
					send: {
						preSend: [validatePermissionsBoundary],
					},
				},
			},
			{
				displayName: 'Tags',
				name: 'tags',
				type: 'fixedCollection',
				description: 'A list of tags that you want to attach to the new user',
				default: [],
				placeholder: 'Add Tag',
				typeOptions: {
					multipleValues: true,
				},
				options: [
					{
						name: 'tags',
						displayName: 'Tag',
						values: [
							{
								displayName: 'Key',
								name: 'key',
								type: 'string',
								default: '',
								placeholder: 'e.g., Department',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								default: '',
								placeholder: 'e.g., Engineering',
							},
						],
					},
				],
				routing: {
					send: {
						preSend: [preprocessTags],
					},
				},
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['user'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
