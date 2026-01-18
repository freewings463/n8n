"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/OpenAiV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/description、../methods、./actions/router、./actions/audio 等5项。导出:OpenAiV2。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/OpenAiV2.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/OpenAiV2_node.py

import {
	NodeConnectionTypes,
	type IExecuteFunctions,
	type INodeType,
	type INodeTypeBaseDescription,
	type INodeTypeDescription,
} from 'n8n-workflow';

import { configureNodeInputs } from '../helpers/description';
import { listSearch, loadOptions } from '../methods';
import { router } from './actions/router';

import * as audio from './actions/audio';
import * as conversation from './actions/conversation';
import * as file from './actions/file';
import * as image from './actions/image';
import * as text from './actions/text';
import * as video from './actions/video';

export class OpenAiV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			version: [2, 2.1],
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
						{
							name: 'Conversation',
							value: 'conversation',
						},
						{
							name: 'Video',
							value: 'video',
						},
					],
					default: 'text',
				},
				...audio.description,
				...file.description,
				...image.description,
				...text.description,
				...conversation.description,
				...video.description,
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
