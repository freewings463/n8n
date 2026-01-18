"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的节点。导入/依赖:外部:@pinecone-database/pinecone、@zilliz/milvus2-sdk-node；内部:n8n-workflow；本地:../VectorStoreQdrant/Qdrant.utils、../VectorStoreWeaviate/Weaviate.utils。导出:无。关键函数/方法:pineconeIndexSearch、results、supabaseTableNameSearch、qdrantCollectionsSearch、milvusCollectionsSearch、weaviateCollectionsSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/methods/listSearch.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/createVectorStoreNode/methods/listSearch.py

import { Pinecone } from '@pinecone-database/pinecone';
import { MilvusClient } from '@zilliz/milvus2-sdk-node';
import { ApplicationError, type IDataObject, type ILoadOptionsFunctions } from 'n8n-workflow';

import type { QdrantCredential } from '../../../VectorStoreQdrant/Qdrant.utils';
import { createQdrantClient } from '../../../VectorStoreQdrant/Qdrant.utils';
import type { WeaviateCredential } from '../../../VectorStoreWeaviate/Weaviate.utils';
import { createWeaviateClient } from '../../../VectorStoreWeaviate/Weaviate.utils';

export async function pineconeIndexSearch(this: ILoadOptionsFunctions) {
	const credentials = await this.getCredentials('pineconeApi');

	const client = new Pinecone({
		apiKey: credentials.apiKey as string,
	});

	const indexes = await client.listIndexes();

	const results = (indexes.indexes ?? []).map((index) => ({
		name: index.name,
		value: index.name,
	}));

	return { results };
}

export async function supabaseTableNameSearch(this: ILoadOptionsFunctions) {
	const credentials = await this.getCredentials('supabaseApi');

	const results = [];

	if (typeof credentials.host !== 'string') {
		throw new ApplicationError('Expected Supabase credentials host to be a string');
	}

	const { paths } = (await this.helpers.requestWithAuthentication.call(this, 'supabaseApi', {
		headers: {
			Prefer: 'return=representation',
		},
		method: 'GET',
		uri: `${credentials.host}/rest/v1/`,
		json: true,
	})) as { paths: IDataObject };

	for (const path of Object.keys(paths)) {
		//omit introspection path
		if (path === '/') continue;

		results.push({
			name: path.replace('/', ''),
			value: path.replace('/', ''),
		});
	}

	return { results };
}

export async function qdrantCollectionsSearch(this: ILoadOptionsFunctions) {
	const credentials = await this.getCredentials('qdrantApi');

	const client = createQdrantClient(credentials as QdrantCredential);

	const response = await client.getCollections();

	const results = response.collections.map((collection) => ({
		name: collection.name,
		value: collection.name,
	}));

	return { results };
}

export async function milvusCollectionsSearch(this: ILoadOptionsFunctions) {
	const credentials = await this.getCredentials<{
		baseUrl: string;
		username: string;
		password: string;
	}>('milvusApi');

	const client = new MilvusClient({
		address: credentials.baseUrl,
		token: `${credentials.username}:${credentials.password}`,
	});

	const response = await client.listCollections();

	const results = response.data.map((collection) => ({
		name: collection.name,
		value: collection.name,
	}));

	return { results };
}

export async function weaviateCollectionsSearch(this: ILoadOptionsFunctions) {
	const credentials = await this.getCredentials('weaviateApi');

	const client = await createWeaviateClient(credentials as WeaviateCredential);

	const collections = await client.collections.listAll();

	const results = collections.map((collection: { name: string }) => ({
		name: collection.name,
		value: collection.name,
	}));

	return { results };
}
