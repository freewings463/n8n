"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePineconeLoad/VectorStorePineconeLoad.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePineconeLoad 的节点。导入/依赖:外部:@langchain/core/embeddings、@langchain/pinecone、@pinecone-database/pinecone、@utils/helpers、@utils/logWrapper、@utils/sharedFields；内部:无；本地:../methods/listSearch、../shared/descriptions。导出:VectorStorePineconeLoad。关键函数/方法:supplyData、embeddings。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePineconeLoad/VectorStorePineconeLoad.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStorePineconeLoad/VectorStorePineconeLoad_node.py

import type { Embeddings } from '@langchain/core/embeddings';
import type { PineconeStoreParams } from '@langchain/pinecone';
import { PineconeStore } from '@langchain/pinecone';
import { Pinecone } from '@pinecone-database/pinecone';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { getMetadataFiltersValues } from '@utils/helpers';
import { logWrapper } from '@utils/logWrapper';
import { metadataFilterField } from '@utils/sharedFields';

import { pineconeIndexSearch } from '../shared/createVectorStoreNode/methods/listSearch';
import { pineconeIndexRLC } from '../shared/descriptions';

// This node is deprecated. Use VectorStorePinecone instead.
export class VectorStorePineconeLoad implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Pinecone: Load',
		// Vector Store nodes got merged into a single node
		hidden: true,
		name: 'vectorStorePineconeLoad',
		icon: 'file:pinecone.svg',
		group: ['transform'],
		version: 1,
		description: 'Load data from Pinecone Vector Store index',
		defaults: {
			name: 'Pinecone: Load',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Vector Stores'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstorepinecone/',
					},
				],
			},
		},
		credentials: [
			{
				name: 'pineconeApi',
				required: true,
			},
		],
		inputs: [
			{
				displayName: 'Embedding',
				maxConnections: 1,
				type: NodeConnectionTypes.AiEmbedding,
				required: true,
			},
		],
		outputs: [NodeConnectionTypes.AiVectorStore],
		outputNames: ['Vector Store'],
		properties: [
			pineconeIndexRLC,
			{
				displayName: 'Pinecone Namespace',
				name: 'pineconeNamespace',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add Option',
				default: {},
				options: [metadataFilterField],
			},
		],
	};

	methods = {
		listSearch: {
			pineconeIndexSearch,
		},
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supplying data for Pinecone Load Vector Store');

		const namespace = this.getNodeParameter('pineconeNamespace', itemIndex) as string;
		const index = this.getNodeParameter('pineconeIndex', itemIndex, '', {
			extractValue: true,
		}) as string;

		const credentials = await this.getCredentials('pineconeApi');
		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			itemIndex,
		)) as Embeddings;

		const client = new Pinecone({
			apiKey: credentials.apiKey as string,
		});

		const pineconeIndex = client.Index(index);
		const config: PineconeStoreParams = {
			namespace: namespace || undefined,
			pineconeIndex,
			filter: getMetadataFiltersValues(this, itemIndex),
		};

		const vectorStore = await PineconeStore.fromExistingIndex(embeddings, config);

		return {
			response: logWrapper(vectorStore, this),
		};
	}
}
