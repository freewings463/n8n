"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/operations/retrieveOperation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的节点。导入/依赖:外部:@langchain/core/embeddings、@langchain/core/…/document_compressors、@langchain/core/vectorstores、@utils/helpers、@utils/logWrapper；内部:n8n-workflow；本地:../types。导出:无。关键函数/方法:reranker。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/operations/retrieveOperation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/createVectorStoreNode/operations/retrieveOperation.py

import type { Embeddings } from '@langchain/core/embeddings';
import type { BaseDocumentCompressor } from '@langchain/core/retrievers/document_compressors';
import type { VectorStore } from '@langchain/core/vectorstores';
import { NodeConnectionTypes, type ISupplyDataFunctions, type SupplyData } from 'n8n-workflow';

import { getMetadataFiltersValues } from '@utils/helpers';
import { logWrapper } from '@utils/logWrapper';

import type { VectorStoreNodeConstructorArgs } from '../types';

/**
 * Handles the 'retrieve' operation mode
 * Returns the vector store to be used with AI nodes
 */
export async function handleRetrieveOperation<T extends VectorStore = VectorStore>(
	context: ISupplyDataFunctions,
	args: VectorStoreNodeConstructorArgs<T>,
	embeddings: Embeddings,
	itemIndex: number,
): Promise<SupplyData> {
	// Get metadata filters
	const filter = getMetadataFiltersValues(context, itemIndex);
	const useReranker = context.getNodeParameter('useReranker', itemIndex, false) as boolean;

	// Get the vector store client
	const vectorStore = await args.getVectorStoreClient(context, filter, embeddings, itemIndex);
	let response: VectorStore | { reranker: BaseDocumentCompressor; vectorStore: VectorStore } =
		vectorStore;

	if (useReranker) {
		const reranker = (await context.getInputConnectionData(
			NodeConnectionTypes.AiReranker,
			0,
		)) as BaseDocumentCompressor;

		// Return reranker and vector store with log wrapper
		response = {
			reranker,
			vectorStore: logWrapper(vectorStore, context),
		};
	} else {
		// Return the vector store with logging wrapper
		response = logWrapper(vectorStore, context);
	}

	return {
		response,
		closeFunction: async () => {
			// Release the vector store client if a release method was provided
			args.releaseVectorStoreClient?.(vectorStore);
		},
	};
}
