"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PostBin/PostBin.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PostBin 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./BinDescription、./RequestDescription。导出:PostBin。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PostBin/PostBin.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PostBin/PostBin_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { binFields, binOperations } from './BinDescription';
import { requestFields, requestOperations } from './RequestDescription';

export class PostBin implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'PostBin',
		name: 'postBin',
		icon: 'file:postbin.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
		description: 'Consume PostBin API',
		defaults: {
			name: 'PostBin',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [],
		requestDefaults: {
			baseURL: 'https://www.postb.in',
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Bin',
						value: 'bin',
					},
					{
						name: 'Request',
						value: 'request',
					},
				],
				default: 'bin',
				required: true,
			},
			...binOperations,
			...binFields,
			...requestOperations,
			...requestFields,
		],
	};
}
