"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreInMemoryInsert/VectorStoreInMemoryInsert.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreInMemoryInsert 的节点。导入/依赖:外部:@langchain/core/embeddings、@langchain/classic/document、@utils/N8nJsonLoader；内部:无；本地:../MemoryManager/MemoryVectorStoreManager、../shared/processDocuments。导出:VectorStoreInMemoryInsert。关键函数/方法:execute、embeddings、documentInput。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreInMemoryInsert/VectorStoreInMemoryInsert.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreInMemoryInsert/VectorStoreInMemoryInsert_node.py

import type { Embeddings } from '@langchain/core/embeddings';
import type { Document } from '@langchain/classic/document';
import {
	NodeConnectionTypes,
	type INodeExecutionData,
	type IExecuteFunctions,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

import type { N8nJsonLoader } from '@utils/N8nJsonLoader';

import { MemoryVectorStoreManager } from '../shared/MemoryManager/MemoryVectorStoreManager';
import { processDocuments } from '../shared/processDocuments';

// This node is deprecated. Use VectorStoreInMemory instead.
export class VectorStoreInMemoryInsert implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'In Memory Vector Store Insert',
		name: 'vectorStoreInMemoryInsert',
		icon: 'fa:database',
		group: ['transform'],
		version: 1,
		hidden: true,
		description: 'Insert data into an in-memory vector store',
		defaults: {
			name: 'In Memory Vector Store Insert',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Vector Stores'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreinmemory/',
					},
				],
			},
		},

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
			{
				displayName:
					'The embbded data are stored in the server memory, so they will be lost when the server is restarted. Additionally, if the amount of data is too large, it may cause the server to crash due to insufficient memory.',
				name: 'notice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Clear Store',
				name: 'clearStore',
				type: 'boolean',
				default: false,
				description: 'Whether to clear the store before inserting new data',
			},
			{
				displayName: 'Memory Key',
				name: 'memoryKey',
				type: 'string',
				default: 'vector_store_key',
				description:
					'The key to use to store the vector memory in the workflow data. The key will be prefixed with the workflow ID to avoid collisions.',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData(0);
		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			0,
		)) as Embeddings;

		const memoryKey = this.getNodeParameter('memoryKey', 0) as string;
		const clearStore = this.getNodeParameter('clearStore', 0) as boolean;
		const documentInput = (await this.getInputConnectionData(NodeConnectionTypes.AiDocument, 0)) as
			| N8nJsonLoader
			| Array<Document<Record<string, unknown>>>;

		const { processedDocuments, serializedDocuments } = await processDocuments(
			documentInput,
			items,
		);

		const workflowId = this.getWorkflow().id;

		const vectorStoreInstance = MemoryVectorStoreManager.getInstance(embeddings, this.logger);
		await vectorStoreInstance.addDocuments(
			`${workflowId}__${memoryKey}`,
			processedDocuments,
			clearStore,
		);

		return [serializedDocuments];
	}
}
