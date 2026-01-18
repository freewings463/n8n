"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabaseInsert/VectorStoreSupabaseInsert.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabaseInsert 的节点。导入/依赖:外部:@langchain/community/…/supabase、@langchain/core/documents、@langchain/core/embeddings、@supabase/supabase-js、@utils/N8nJsonLoader；内部:无；本地:../methods/listSearch、../shared/descriptions、../shared/processDocuments。导出:VectorStoreSupabaseInsert。关键函数/方法:execute、documentInput、embeddings。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabaseInsert/VectorStoreSupabaseInsert.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreSupabaseInsert/VectorStoreSupabaseInsert_node.py

import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import type { Document } from '@langchain/core/documents';
import type { Embeddings } from '@langchain/core/embeddings';
import { createClient } from '@supabase/supabase-js';
import {
	type IExecuteFunctions,
	type INodeType,
	type INodeTypeDescription,
	type INodeExecutionData,
	NodeConnectionTypes,
} from 'n8n-workflow';

import type { N8nJsonLoader } from '@utils/N8nJsonLoader';

import { supabaseTableNameSearch } from '../shared/createVectorStoreNode/methods/listSearch';
import { supabaseTableNameRLC } from '../shared/descriptions';
import { processDocuments } from '../shared/processDocuments';

// This node is deprecated. Use VectorStoreSupabase instead.
export class VectorStoreSupabaseInsert implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Supabase: Insert',
		// Vector Store nodes got merged into a single node
		hidden: true,
		name: 'vectorStoreSupabaseInsert',
		icon: 'file:supabase.svg',
		group: ['transform'],
		version: 1,
		description:
			'Insert data into Supabase Vector Store index [https://supabase.com/docs/guides/ai/langchain]',
		defaults: {
			name: 'Supabase: Insert',
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
					'Please refer to the <a href="https://supabase.com/docs/guides/ai/langchain" target="_blank">Supabase documentation</a> for more information on how to setup your database as a Vector Store.',
				name: 'setupNotice',
				type: 'notice',
				default: '',
			},
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
				displayName: 'Specify the document to load in the document loader sub-node',
				name: 'notice',
				type: 'notice',
				default: '',
			},
		],
	};

	methods = { listSearch: { supabaseTableNameSearch } };

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		this.logger.debug('Executing data for Supabase Insert Vector Store');

		const items = this.getInputData(0);
		const tableName = this.getNodeParameter('tableName', 0, '', { extractValue: true }) as string;
		const queryName = this.getNodeParameter('queryName', 0) as string;
		const credentials = await this.getCredentials('supabaseApi');

		const documentInput = (await this.getInputConnectionData(NodeConnectionTypes.AiDocument, 0)) as
			| N8nJsonLoader
			| Array<Document<Record<string, unknown>>>;

		const embeddings = (await this.getInputConnectionData(
			NodeConnectionTypes.AiEmbedding,
			0,
		)) as Embeddings;
		const client = createClient(credentials.host as string, credentials.serviceRole as string);

		const { processedDocuments, serializedDocuments } = await processDocuments(
			documentInput,
			items,
		);

		await SupabaseVectorStore.fromDocuments(processedDocuments, embeddings, {
			client,
			tableName,
			queryName,
		});

		return [serializedDocuments];
	}
}
