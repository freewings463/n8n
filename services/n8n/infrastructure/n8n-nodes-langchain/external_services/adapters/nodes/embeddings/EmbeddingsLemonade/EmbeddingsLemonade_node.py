"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsLemonade/EmbeddingsLemonade.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsLemonade 的节点。导入/依赖:外部:@langchain/openai、@utils/logWrapper、@utils/sharedFields；内部:无；本地:../credentials/LemonadeApi.credentials、../LMLemonade/description。导出:EmbeddingsLemonade。关键函数/方法:supplyData、credentials。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsLemonade/EmbeddingsLemonade.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/embeddings/EmbeddingsLemonade/EmbeddingsLemonade_node.py

import { OpenAIEmbeddings } from '@langchain/openai';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import type { LemonadeApiCredentialsType } from '../../../credentials/LemonadeApi.credentials';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

import { lemonadeDescription, lemonadeModel } from '../../llms/LMLemonade/description';

export class EmbeddingsLemonade implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Embeddings Lemonade',
		name: 'embeddingsLemonade',
		icon: 'file:lemonade.svg',
		group: ['transform'],
		version: 1,
		description: 'Use Lemonade Embeddings',
		defaults: {
			name: 'Embeddings Lemonade',
		},
		...lemonadeDescription,
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Embeddings'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.embeddingslemonade/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiEmbedding],
		outputNames: ['Embeddings'],
		properties: [getConnectionHintNoticeField([NodeConnectionTypes.AiVectorStore]), lemonadeModel],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const modelName = this.getNodeParameter('model', itemIndex) as string;
		const credentials = (await this.getCredentials('lemonadeApi')) as LemonadeApiCredentialsType;

		// Ensure we have an API key for OpenAI client validation
		const apiKey = credentials.apiKey || 'lemonade-placeholder-key';

		// Build configuration object separately like official OpenAI nodes
		const configuration: any = {
			baseURL: credentials.baseUrl,
		};

		// Add custom headers if API key is provided
		if (credentials.apiKey) {
			configuration.defaultHeaders = {
				Authorization: `Bearer ${credentials.apiKey}`,
			};
		}

		const embeddings = new OpenAIEmbeddings({
			apiKey,
			model: modelName,
			configuration,
		});

		return {
			response: logWrapper(embeddings, this),
		};
	}
}
