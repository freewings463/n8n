"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/OpenAiV1.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:无；本地:../methods、./actions/router、../helpers/description、./actions/assistant 等4项。导出:OpenAiV1。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/OpenAiV1.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/OpenAiV1_node.py

import {
	NodeConnectionTypes,
	type IExecuteFunctions,
	type INodeType,
	type INodeTypeBaseDescription,
	type INodeTypeDescription,
} from 'n8n-workflow';

import { listSearch, loadOptions } from '../methods';
import { router } from './actions/router';
import { configureNodeInputs } from '../helpers/description';

import * as assistant from './actions/assistant';
import * as audio from './actions/audio';
import * as file from './actions/file';
import * as image from './actions/image';
import * as text from './actions/text';

export class OpenAiV1 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			version: [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
			defaults: {
				name: 'OpenAI',
			},
			inputs: `={{(${configureNodeInputs})($parameter.resource, $parameter.operation, $parameter.hideTools, $parameter.memory ?? undefined)}}`,
			outputs: [NodeConnectionTypes.Main],
			credentials: [
				{
					name: 'openAiApi',
					required: true,
				},
			],
			properties: [
				{
					displayName: 'Resource',
					name: 'resource',
					type: 'options',
					noDataExpression: true,
					// eslint-disable-next-line n8n-nodes-base/node-param-options-type-unsorted-items
					options: [
						{
							name: 'Assistant',
							value: 'assistant',
						},
						{
							name: 'Text',
							value: 'text',
						},
						{
							name: 'Image',
							value: 'image',
						},
						{
							name: 'Audio',
							value: 'audio',
						},
						{
							name: 'File',
							value: 'file',
						},
					],
					default: 'text',
				},
				...assistant.description,
				...audio.description,
				...file.description,
				...image.description,
				...text.description,
			],
		};
	}

	methods = {
		listSearch,
		loadOptions,
	};

	async execute(this: IExecuteFunctions) {
		return await router.call(this);
	}
}
