"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/AwsCognito.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./descriptions、./helpers/utils、./methods。导出:AwsCognito。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/AwsCognito.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/AwsCognito_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { group, user, userPool } from './descriptions';
import { preSendStringifyBody } from './helpers/utils';
import { listSearch } from './methods';

export class AwsCognito implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'AWS Cognito',
		name: 'awsCognito',
		icon: {
			light: 'file:cognito.svg',
			dark: 'file:cognito.svg',
		},
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Sends data to AWS Cognito',
		defaults: {
			name: 'AWS Cognito',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'aws',
				required: true,
			},
		],
		requestDefaults: {
			headers: {
				'Content-Type': 'application/x-amz-json-1.1',
			},
			qs: {
				service: 'cognito-idp',
				_region: '={{$credentials.region}}',
			},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				default: 'user',
				routing: {
					send: {
						preSend: [preSendStringifyBody],
					},
				},
				options: [
					{
						name: 'Group',
						value: 'group',
					},
					{
						name: 'User',
						value: 'user',
					},
					{
						name: 'User Pool',
						value: 'userPool',
					},
				],
			},
			...group.description,
			...user.description,
			...userPool.description,
		],
	};

	methods = {
		listSearch,
	};
}
