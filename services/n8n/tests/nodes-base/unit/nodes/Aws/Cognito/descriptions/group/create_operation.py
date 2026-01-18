"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/descriptions/group/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common.description。导出:description。关键函数/方法:function。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/descriptions/group/create.operation.ts -> services/n8n/tests/nodes-base/unit/nodes/Aws/Cognito/descriptions/group/create_operation.py

import type { IExecuteSingleFunctions, IHttpRequestOptions, INodeProperties } from 'n8n-workflow';
import { NodeApiError, updateDisplayOptions } from 'n8n-workflow';

import { validateArn } from '../../helpers/utils';
import { userPoolResourceLocator } from '../common.description';

const properties: INodeProperties[] = [
	{
		...userPoolResourceLocator,
		description: 'Select the user pool to use',
	},
	{
		displayName: 'Group Name',
		name: 'newGroupName',
		default: '',
		placeholder: 'e.g. MyNewGroup',
		description: 'The name of the new group to create',
		required: true,
		type: 'string',
		validateType: 'string',
		routing: {
			send: {
				property: 'GroupName',
				type: 'body',
				preSend: [
					async function (
						this: IExecuteSingleFunctions,
						requestOptions: IHttpRequestOptions,
					): Promise<IHttpRequestOptions> {
						const newGroupName = this.getNodeParameter('newGroupName', '') as string;
						const groupNameRegex = /^[\p{L}\p{M}\p{S}\p{N}\p{P}]+$/u;
						if (!groupNameRegex.test(newGroupName)) {
							throw new NodeApiError(this.getNode(), {
								message: 'Invalid format for Group Name',
								description: 'Group Name should not contain spaces.',
							});
						}
						return requestOptions;
					},
				],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		default: {},
		options: [
			{
				displayName: 'Description',
				name: 'description',
				default: '',
				placeholder: 'e.g. New group description',
				description: 'A description for the new group',
				type: 'string',
				routing: {
					send: {
						type: 'body',
						property: 'Description',
					},
				},
			},
			{
				displayName: 'Precedence',
				name: 'precedence',
				default: '',
				placeholder: 'e.g. 10',
				description: 'Precedence value for the group. Lower values indicate higher priority.',
				type: 'number',
				routing: {
					send: {
						type: 'body',
						property: 'Precedence',
					},
				},
				validateType: 'number',
			},
			{
				displayName: 'Role ARN',
				name: 'arn',
				default: '',
				placeholder: 'e.g. arn:aws:iam::123456789012:role/GroupRole',
				description: 'The role ARN for the group, used for setting claims in tokens',
				type: 'string',
				routing: {
					send: {
						type: 'body',
						property: 'Arn',
						preSend: [validateArn],
					},
				},
			},
		],
		placeholder: 'Add Option',
		type: 'collection',
	},
];

const displayOptions = {
	show: {
		resource: ['group'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
