"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabaseLoad/VectorStoreSupabaseLoad.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabaseLoad 的节点。导入/依赖:外部:@langchain/community/…/supabase、@langchain/core/embeddings、@supabase/supabase-js、@utils/helpers、@utils/logWrapper、@utils/sharedFields；内部:无；本地:../methods/listSearch、../shared/descriptions。导出:VectorStoreSupabaseLoad。关键函数/方法:supplyData、embeddings。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabaseLoad/VectorStoreSupabaseLoad.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreSupabaseLoad/VectorStoreSupabaseLoad_node.py

import type { SupabaseLibArgs } from '@langchain/community/vectorstores/supabase';
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import type { Embeddings } from '@langchain/core/embeddings';
import { createClient } from '@supabase/supabase-js';
import {
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { getMetadataFiltersValues } from '@utils/helpers';
import { logWrapper } from '@utils/logWrapper';
import { metadataFilterField } from '@utils/sharedFields';

import { supabaseTableNameSearch } from '../shared/createVectorStoreNode/methods/listSearch';
import { supabaseTableNameRLC } from '../shared/descriptions';

// This node is deprecated. Use VectorStoreSupabase instead.
export class VectorStoreSupabaseLoad implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Supabase: Load',
		name: 'vectorStoreSupabaseLoad',
		icon: 'file:supabase.svg',
		// Vector Store nodes got merged into a single node
		hidden: true,
		group: ['transform'],
		version: 1,
		description: 'Load data from Supabase Vector Store index',
		defaults: {
			name: 'Supabase: Load',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Vector Stores'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoresupabase/',
					},
				],
			},
		},
		credentials: [
			{
				name: 'supabaseApi',
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
			supabaseTableNameRLC,
			{
				displayName: 'Query Name',
				name: 'queryName',
				type: 'string',
				default: 'match_documents',
				required: true,
				description: 'Name of the query to use for matching documents',
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

	methods = { listSearch: { supabaseTableNameSearch } };

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply Supabase Load Vector Store');

		const tableName = this.getNodeParameter('tableName', itemIndex, '', {
			extractValue: true,
		}) as string;
		const queryName = this.getNodeParameter('queryName', itemIndex) as string;

		const credentials = await this.getCredentials('supabaseApi');
		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			0,
		)) as Embeddings;

		const client = createClient(credentials.host as string, credentials.serviceRole as string);
		const config: SupabaseLibArgs = {
			client,
			tableName,
			queryName,
			filter: getMetadataFiltersValues(this, itemIndex),
		};

		const vectorStore = await SupabaseVectorStore.fromExistingIndex(embeddings, config);

		return {
			response: logWrapper(vectorStore, this),
		};
	}
}
