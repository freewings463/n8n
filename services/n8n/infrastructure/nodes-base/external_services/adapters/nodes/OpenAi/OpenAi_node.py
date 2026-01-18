"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/OpenAi/OpenAi.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./ChatDescription、./ImageDescription、./TextDescription、../utils/descriptions。导出:OpenAi。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/OpenAi/OpenAi.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/OpenAi/OpenAi_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { chatFields, chatOperations } from './ChatDescription';
import { imageFields, imageOperations } from './ImageDescription';
import { textFields, textOperations } from './TextDescription';
import { oldVersionNotice } from '../../utils/descriptions';

export class OpenAi implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'OpenAI',
		name: 'openAi',
		hidden: true,
		icon: { light: 'file:openAi.svg', dark: 'file:openAi.dark.svg' },
		group: ['transform'],
		version: [1, 1.1],
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Open AI',
		defaults: {
			name: 'OpenAI',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'openAiApi',
				required: true,
			},
		],
		requestDefaults: {
			ignoreHttpStatusErrors: true,
			baseURL:
				'={{ $credentials.url?.split("/").slice(0,-1).join("/") ?? "https://api.openai.com" }}',
		},
		properties: [
			oldVersionNotice,
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Chat',
						value: 'chat',
					},
					{
						name: 'Image',
						value: 'image',
					},
					{
						name: 'Text',
						value: 'text',
					},
				],
				default: 'text',
			},

			...chatOperations,
			...chatFields,

			...imageOperations,
			...imageFields,

			...textOperations,
			...textFields,
		],
	};
}
