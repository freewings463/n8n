"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Npm/Npm.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Npm 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./DistTagDescription、./PackageDescription。导出:Npm。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Npm/Npm.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Npm/Npm_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { distTagFields, distTagOperations } from './DistTagDescription';
import { packageFields, packageOperations } from './PackageDescription';

export class Npm implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Npm',
		name: 'npm',
		icon: 'file:npm.svg',
		group: ['input'],
		version: 1,
		subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
		description: 'Consume NPM registry API',
		defaults: {
			name: 'npm',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'npmApi',
				required: false,
			},
		],
		requestDefaults: {
			baseURL: '={{ $credentials.registryUrl }}',
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Package',
						value: 'package',
					},
					{
						name: 'Distribution Tag',
						value: 'distTag',
					},
				],
				default: 'package',
			},

			...packageOperations,
			...packageFields,

			...distTagOperations,
			...distTagFields,
		],
	};
}
