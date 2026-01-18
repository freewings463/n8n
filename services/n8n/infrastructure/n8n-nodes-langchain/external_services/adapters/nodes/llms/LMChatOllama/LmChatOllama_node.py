"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LMChatOllama/LmChatOllama.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LMChatOllama 的节点。导入/依赖:外部:@langchain/ollama、@utils/sharedFields；内部:无；本地:../LMOllama/description、../n8nLlmFailedAttemptHandler、../N8nLlmTracing。导出:LmChatOllama。关键函数/方法:getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LMChatOllama/LmChatOllama.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LMChatOllama/LmChatOllama_node.py

import type { ChatOllamaInput } from '@langchain/ollama';
import { ChatOllama } from '@langchain/ollama';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { getConnectionHintNoticeField } from '@utils/sharedFields';

import { ollamaModel, ollamaOptions, ollamaDescription } from '../LMOllama/description';
import { makeN8nLlmFailedAttemptHandler } from '../n8nLlmFailedAttemptHandler';
import { N8nLlmTracing } from '../N8nLlmTracing';

export class LmChatOllama implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Ollama Chat Model',

		name: 'lmChatOllama',
		icon: 'file:ollama.svg',
		group: ['transform'],
		version: 1,
		description: 'Language Model Ollama',
		defaults: {
			name: 'Ollama Chat Model',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Language Models', 'Root Nodes'],
				'Language Models': ['Chat Models (Recommended)'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatollama/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiLanguageModel],
		outputNames: ['Model'],
		...ollamaDescription,
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiChain, NodeConnectionTypes.AiAgent]),
			ollamaModel,
			ollamaOptions,
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const credentials = await this.getCredentials('ollamaApi');

		const modelName = this.getNodeParameter('model', itemIndex) as string;
		const options = this.getNodeParameter('options', itemIndex, {}) as ChatOllamaInput;
		const headers = credentials.apiKey
			? {
					Authorization: `Bearer ${credentials.apiKey as string}`,
				}
			: undefined;

		const model = new ChatOllama({
			...options,
			baseUrl: credentials.baseUrl as string,
			model: modelName,
			format: options.format === 'default' ? undefined : options.format,
			callbacks: [new N8nLlmTracing(this)],
			onFailedAttempt: makeN8nLlmFailedAttemptHandler(this),
			headers,
		});

		return {
			response: model,
		};
	}
}
