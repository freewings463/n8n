"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/rerankers/RerankerCohere/RerankerCohere.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/rerankers/RerankerCohere 的节点。导入/依赖:外部:@langchain/cohere、@utils/logWrapper；内部:无；本地:无。导出:RerankerCohere。关键函数/方法:supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/rerankers/RerankerCohere/RerankerCohere.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/rerankers/RerankerCohere/RerankerCohere_node.py

import { CohereRerank } from '@langchain/cohere';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';

export class RerankerCohere implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Reranker Cohere',
		name: 'rerankerCohere',
		icon: { light: 'file:cohere.svg', dark: 'file:cohere.dark.svg' },
		group: ['transform'],
		version: 1,
		description:
			'Use Cohere Reranker to reorder documents after retrieval from a vector store by relevance to the given query.',
		defaults: {
			name: 'Reranker Cohere',
		},
		requestDefaults: {
			ignoreHttpStatusErrors: true,
			baseURL: '={{ $credentials.host }}',
		},
		credentials: [
			{
				name: 'cohereApi',
				required: true,
			},
		],
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Rerankers'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.rerankercohere/',
					},
				],
			},
		},
		inputs: [],
		outputs: [NodeConnectionTypes.AiReranker],
		outputNames: ['Reranker'],
		properties: [
			{
				displayName: 'Model',
				name: 'modelName',
				type: 'options',
				description:
					'The model that should be used to rerank the documents. <a href="https://docs.cohere.com/docs/models">Learn more</a>.',
				default: 'rerank-v3.5',
				options: [
					{
						name: 'rerank-v3.5',
						value: 'rerank-v3.5',
					},
					{
						name: 'rerank-english-v3.0',
						value: 'rerank-english-v3.0',
					},
					{
						name: 'rerank-multilingual-v3.0',
						value: 'rerank-multilingual-v3.0',
					},
				],
			},
			{
				displayName: 'Top N',
				name: 'topN',
				type: 'number',
				description: 'The maximum number of documents to return after reranking',
				default: 3,
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply data for reranking Cohere');
		const modelName = this.getNodeParameter('modelName', itemIndex, 'rerank-v3.5') as string;
		const topN = this.getNodeParameter('topN', itemIndex, 3) as number;
		const credentials = await this.getCredentials<{ apiKey: string }>('cohereApi');

		const reranker = new CohereRerank({
			apiKey: credentials.apiKey,
			model: modelName,
			topN,
		});

		return {
			response: logWrapper(reranker, this),
		};
	}
}
