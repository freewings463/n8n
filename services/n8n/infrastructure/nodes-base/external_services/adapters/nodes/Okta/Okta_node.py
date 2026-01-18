"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Okta/Okta.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Okta 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./UserDescription、./UserFunctions。导出:Okta。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Okta/Okta.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Okta/Okta_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { userFields, userOperations } from './UserDescription';
import { getUsers } from './UserFunctions';

export class Okta implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Okta',
		name: 'okta',
		icon: { light: 'file:Okta.svg', dark: 'file:Okta.dark.svg' },
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Use the Okta API',
		defaults: {
			name: 'Okta',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'oktaApi',
				required: true,
			},
		],
		requestDefaults: {
			returnFullResponse: true,
			baseURL: '={{$credentials.url.replace(new RegExp("/$"), "")}}',
			headers: {},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'User',
						value: 'user',
					},
				],
				default: 'user',
			},

			// USER
			...userOperations,
			...userFields,
		],
	};

	methods = {
		listSearch: {
			getUsers,
		},
	};
}
