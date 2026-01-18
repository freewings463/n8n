"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreZepLoad/VectorStoreZepLoad.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreZepLoad 的节点。导入/依赖:外部:@langchain/community/…/zep、@langchain/core/embeddings、@utils/helpers、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:VectorStoreZepLoad。关键函数/方法:supplyData、embeddings。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreZepLoad/VectorStoreZepLoad.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreZepLoad/VectorStoreZepLoad_node.py

import type { IZepConfig } from '@langchain/community/vectorstores/zep';
import { ZepVectorStore } from '@langchain/community/vectorstores/zep';
import type { Embeddings } from '@langchain/core/embeddings';
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

// This node is deprecated. Use VectorStoreZep instead.
export class VectorStoreZepLoad implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Zep Vector Store: Load',
		name: 'vectorStoreZepLoad',
		hidden: true,
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:zep.png',
		group: ['transform'],
		version: 1,
		description: 'Load data from Zep Vector Store index',
		defaults: {
			name: 'Zep: Load',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Vector Stores'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstorezep/',
					},
				],
			},
		},
		credentials: [
			{
				name: 'zepApi',
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
			{
				displayName: 'This Zep integration is deprecated and will be removed in a future version.',
				name: 'deprecationNotice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Collection Name',
				name: 'collectionName',
				type: 'string',
				default: '',
				required: true,
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add Option',
				default: {},
				options: [
					{
						displayName: 'Embedding Dimensions',
						name: 'embeddingDimensions',
						type: 'number',
						default: 1536,
						description: 'Whether to allow using characters from the Unicode surrogate blocks',
					},
					metadataFilterField,
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supplying data for Zep Load Vector Store');

		const collectionName = this.getNodeParameter('collectionName', itemIndex) as string;

		const options =
			(this.getNodeParameter('options', itemIndex) as {
				embeddingDimensions?: number;
			}) || {};

		const credentials = await this.getCredentials<{
			apiKey?: string;
			apiUrl: string;
		}>('zepApi');
		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			0,
		)) as Embeddings;

		const zepConfig: IZepConfig = {
			apiUrl: credentials.apiUrl,
			apiKey: credentials.apiKey,
			collectionName,
			embeddingDimensions: options.embeddingDimensions ?? 1536,
			metadata: getMetadataFiltersValues(this, itemIndex),
		};

		const vectorStore = new ZepVectorStore(embeddings, zepConfig);

		return {
			response: logWrapper(vectorStore, this),
		};
	}
}
