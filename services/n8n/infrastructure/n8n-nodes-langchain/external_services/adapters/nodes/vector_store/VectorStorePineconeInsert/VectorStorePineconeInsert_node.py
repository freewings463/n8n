"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePineconeInsert/VectorStorePineconeInsert.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePineconeInsert 的节点。导入/依赖:外部:@langchain/core/documents、@langchain/core/embeddings、@langchain/pinecone、@pinecone-database/pinecone、@utils/N8nJsonLoader；内部:无；本地:../methods/listSearch、../shared/descriptions、../shared/processDocuments。导出:VectorStorePineconeInsert。关键函数/方法:execute、documentInput、embeddings。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePineconeInsert/VectorStorePineconeInsert.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStorePineconeInsert/VectorStorePineconeInsert_node.py

import type { Document } from '@langchain/core/documents';
import type { Embeddings } from '@langchain/core/embeddings';
import { PineconeStore } from '@langchain/pinecone';
import { Pinecone } from '@pinecone-database/pinecone';
import {
	type IExecuteFunctions,
	type INodeType,
	type INodeTypeDescription,
	type INodeExecutionData,
	NodeConnectionTypes,
} from 'n8n-workflow';

import type { N8nJsonLoader } from '@utils/N8nJsonLoader';

import { pineconeIndexSearch } from '../shared/createVectorStoreNode/methods/listSearch';
import { pineconeIndexRLC } from '../shared/descriptions';
import { processDocuments } from '../shared/processDocuments';

// This node is deprecated. Use VectorStorePinecone instead.
export class VectorStorePineconeInsert implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Pinecone: Insert',
		hidden: true,
		name: 'vectorStorePineconeInsert',
		icon: 'file:pinecone.svg',
		group: ['transform'],
		version: 1,
		description: 'Insert data into Pinecone Vector Store index',
		defaults: {
			name: 'Pinecone: Insert',
			// eslint-disable-next-line n8n-nodes-base/node-class-description-non-core-color-present
			color: '#1321A7',
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
			NodeConnectionTypes.Main,
			{
				displayName: 'Document',
				maxConnections: 1,
				type: NodeConnectionTypes.AiDocument,
				required: true,
			},
			{
				displayName: 'Embedding',
				maxConnections: 1,
				type: NodeConnectionTypes.AiEmbedding,
				required: true,
			},
		],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			pineconeIndexRLC,
			{
				displayName: 'Pinecone Namespace',
				name: 'pineconeNamespace',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Specify the document to load in the document loader sub-node',
				name: 'notice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Clear Namespace',
				name: 'clearNamespace',
				type: 'boolean',
				default: false,
				description: 'Whether to clear the namespace before inserting new data',
			},
		],
	};

	methods = {
		listSearch: {
			pineconeIndexSearch,
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData(0);
		this.logger.debug('Executing data for Pinecone Insert Vector Store');

		const namespace = this.getNodeParameter('pineconeNamespace', 0) as string;
		const index = this.getNodeParameter('pineconeIndex', 0, '', { extractValue: true }) as string;
		const clearNamespace = this.getNodeParameter('clearNamespace', 0) as boolean;

		const credentials = await this.getCredentials('pineconeApi');

		const documentInput = (await this.getInputConnectionData(NodeConnectionTypes.AiDocument, 0)) as
			| N8nJsonLoader
			| Array<Document<Record<string, unknown>>>;

		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			0,
		)) as Embeddings;

		const client = new Pinecone({
			apiKey: credentials.apiKey as string,
		});

		const pineconeIndex = client.Index(index);

		if (namespace && clearNamespace) {
			await pineconeIndex.namespace(namespace).deleteAll();
		}

		const { processedDocuments, serializedDocuments } = await processDocuments(
			documentInput,
			items,
		);

		await PineconeStore.fromDocuments(processedDocuments, embeddings, {
			namespace: namespace || undefined,
			pineconeIndex,
		});

		return [serializedDocuments];
	}
}
