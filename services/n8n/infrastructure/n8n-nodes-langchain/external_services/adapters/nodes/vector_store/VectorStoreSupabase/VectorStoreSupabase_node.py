"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabase/VectorStoreSupabase.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabase 的节点。导入/依赖:外部:@langchain/community/…/supabase、@supabase/supabase-js、@utils/sharedFields；内部:n8n-workflow；本地:../createVectorStoreNode/createVectorStoreNode、../methods/listSearch、../shared/descriptions。导出:VectorStoreSupabase。关键函数/方法:getVectorStoreClient、populateVectorStore。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreSupabase/VectorStoreSupabase.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreSupabase/VectorStoreSupabase_node.py

import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import { createClient } from '@supabase/supabase-js';
import { NodeOperationError, type INodeProperties } from 'n8n-workflow';

import { metadataFilterField } from '@utils/sharedFields';

import { createVectorStoreNode } from '../shared/createVectorStoreNode/createVectorStoreNode';
import { supabaseTableNameSearch } from '../shared/createVectorStoreNode/methods/listSearch';
import { supabaseTableNameRLC } from '../shared/descriptions';

const queryNameField: INodeProperties = {
	displayName: 'Query Name',
	name: 'queryName',
	type: 'string',
	default: 'match_documents',
	description: 'Name of the query to use for matching documents',
};

const sharedFields: INodeProperties[] = [supabaseTableNameRLC];
const insertFields: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [queryNameField],
	},
];

const retrieveFields: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [queryNameField, metadataFilterField],
	},
];

const updateFields: INodeProperties[] = [...insertFields];

export class VectorStoreSupabase extends createVectorStoreNode<SupabaseVectorStore>({
	meta: {
		description: 'Work with your data in Supabase Vector Store',
		icon: 'file:supabase.svg',
		displayName: 'Supabase Vector Store',
		docsUrl:
			'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoresupabase/',
		name: 'vectorStoreSupabase',
		credentials: [
			{
				name: 'supabaseApi',
				required: true,
			},
		],
		operationModes: ['load', 'insert', 'retrieve', 'update', 'retrieve-as-tool'],
	},
	methods: {
		listSearch: { supabaseTableNameSearch },
	},
	sharedFields,
	insertFields,
	loadFields: retrieveFields,
	retrieveFields,
	updateFields,
	async getVectorStoreClient(context, filter, embeddings, itemIndex) {
		const tableName = context.getNodeParameter('tableName', itemIndex, '', {
			extractValue: true,
		}) as string;
		const options = context.getNodeParameter('options', itemIndex, {}) as {
			queryName: string;
		};
		const credentials = await context.getCredentials('supabaseApi');
		const client = createClient(credentials.host as string, credentials.serviceRole as string);

		return await SupabaseVectorStore.fromExistingIndex(embeddings, {
			client,
			tableName,
			queryName: options.queryName ?? 'match_documents',
			filter,
		});
	},
	async populateVectorStore(context, embeddings, documents, itemIndex) {
		const tableName = context.getNodeParameter('tableName', itemIndex, '', {
			extractValue: true,
		}) as string;
		const options = context.getNodeParameter('options', itemIndex, {}) as {
			queryName: string;
		};
		const credentials = await context.getCredentials('supabaseApi');
		const client = createClient(credentials.host as string, credentials.serviceRole as string);

		try {
			await SupabaseVectorStore.fromDocuments(documents, embeddings, {
				client,
				tableName,
				queryName: options.queryName ?? 'match_documents',
			});
		} catch (error) {
			if ((error as Error).message === 'Error inserting: undefined 404 Not Found') {
				throw new NodeOperationError(context.getNode(), `Table ${tableName} not found`, {
					itemIndex,
					description: 'Please check that the table exists in your vector store',
				});
			} else {
				throw new NodeOperationError(context.getNode(), error as Error, {
					itemIndex,
				});
			}
		}
	},
}) {}
