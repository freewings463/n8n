"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsOllama/EmbeddingsOllama.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsOllama 的节点。导入/依赖:外部:@langchain/ollama、@utils/logWrapper、@utils/sharedFields；内部:无；本地:../LMOllama/description。导出:EmbeddingsOllama。关键函数/方法:supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsOllama/EmbeddingsOllama.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/embeddings/EmbeddingsOllama/EmbeddingsOllama_node.py

import { OllamaEmbeddings } from '@langchain/ollama';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

import { ollamaDescription, ollamaModel } from '../../llms/LMOllama/description';

export class EmbeddingsOllama implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Embeddings Ollama',
		name: 'embeddingsOllama',
		icon: 'file:ollama.svg',
		group: ['transform'],
		version: 1,
		description: 'Use Ollama Embeddings',
		defaults: {
			name: 'Embeddings Ollama',
		},
		...ollamaDescription,
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Embeddings'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.embeddingsollama/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiEmbedding],
		outputNames: ['Embeddings'],
		properties: [getConnectionHintNoticeField([NodeConnectionTypes.AiVectorStore]), ollamaModel],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply data for embeddings Ollama');
		const modelName = this.getNodeParameter('model', itemIndex) as string;
		const credentials = await this.getCredentials('ollamaApi');
		const headers = credentials.apiKey
			? {
					Authorization: `Bearer ${credentials.apiKey as string}`,
				}
			: undefined;

		const embeddings = new OllamaEmbeddings({
			baseUrl: credentials.baseUrl as string,
			model: modelName,
			headers,
		});

		return {
			response: logWrapper(embeddings, this),
		};
	}
}
