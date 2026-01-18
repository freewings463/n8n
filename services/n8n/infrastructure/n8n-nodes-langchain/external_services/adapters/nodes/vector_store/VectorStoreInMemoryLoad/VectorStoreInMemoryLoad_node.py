"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreInMemoryLoad/VectorStoreInMemoryLoad.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreInMemoryLoad 的节点。导入/依赖:外部:@langchain/core/embeddings、@utils/logWrapper；内部:无；本地:../MemoryManager/MemoryVectorStoreManager。导出:VectorStoreInMemoryLoad。关键函数/方法:supplyData、embeddings。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreInMemoryLoad/VectorStoreInMemoryLoad.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreInMemoryLoad/VectorStoreInMemoryLoad_node.py

import type { Embeddings } from '@langchain/core/embeddings';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';

import { MemoryVectorStoreManager } from '../shared/MemoryManager/MemoryVectorStoreManager';

// This node is deprecated. Use VectorStoreInMemory instead.
export class VectorStoreInMemoryLoad implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'In Memory Vector Store Load',
		name: 'vectorStoreInMemoryLoad',
		icon: 'fa:database',
		group: ['transform'],
		version: 1,
		hidden: true,
		description: 'Load embedded data from an in-memory vector store',
		defaults: {
			name: 'In Memory Vector Store Load',
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

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			itemIndex,
		)) as Embeddings;

		const workflowId = this.getWorkflow().id;
		const memoryKey = this.getNodeParameter('memoryKey', 0) as string;

		const vectorStoreSingleton = MemoryVectorStoreManager.getInstance(embeddings, this.logger);
		const vectorStoreInstance = await vectorStoreSingleton.getVectorStore(
			`${workflowId}__${memoryKey}`,
		);

		return {
			response: logWrapper(vectorStoreInstance, this),
		};
	}
}
