"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverVectorStore/RetrieverVectorStore.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverVectorStore 的Store。导入/依赖:外部:@langchain/core/…/document_compressors、@langchain/core/vectorstores、@langchain/classic/…/contextual_compression、@utils/logWrapper；内部:无；本地:无。导出:RetrieverVectorStore。关键函数/方法:supplyData、vectorStore。用于管理该模块前端状态（state/actions/getters）供UI消费。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverVectorStore/RetrieverVectorStore.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/retrievers/RetrieverVectorStore/RetrieverVectorStore_node.py

import type { BaseDocumentCompressor } from '@langchain/core/retrievers/document_compressors';
import { VectorStore } from '@langchain/core/vectorstores';
import { ContextualCompressionRetriever } from '@langchain/classic/retrievers/contextual_compression';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';

export class RetrieverVectorStore implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Vector Store Retriever',
		name: 'retrieverVectorStore',
		icon: 'fa:box-open',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description: 'Use a Vector Store as Retriever',
		defaults: {
			name: 'Vector Store Retriever',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Retrievers'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.retrievervectorstore/',
					},
				],
			},
		},

		inputs: [
			{
				displayName: 'Vector Store',
				maxConnections: 1,
				type: NodeConnectionTypes.AiVectorStore,
				required: true,
			},
		],

		outputs: [NodeConnectionTypes.AiRetriever],
		outputNames: ['Retriever'],
		properties: [
			{
				displayName: 'Limit',
				name: 'topK',
				type: 'number',
				default: 4,
				description: 'The maximum number of results to return',
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supplying data for Vector Store Retriever');

		const topK = this.getNodeParameter('topK', itemIndex, 4) as number;
		const vectorStore = (await this.getInputConnectionData(
			NodeConnectionTypes.AiVectorStore,
			itemIndex,
		)) as
			| VectorStore
			| {
					reranker: BaseDocumentCompressor;
					vectorStore: VectorStore;
			  };

		let retriever = null;

		if (vectorStore instanceof VectorStore) {
			retriever = vectorStore.asRetriever(topK);
		} else {
			retriever = new ContextualCompressionRetriever({
				baseCompressor: vectorStore.reranker,
				baseRetriever: vectorStore.vectorStore.asRetriever(topK),
			});
		}

		return {
			response: logWrapper(retriever, this),
		};
	}
}
