"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePinecone/VectorStorePinecone.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePinecone 的节点。导入/依赖:外部:@langchain/pinecone、@pinecone-database/pinecone、@utils/sharedFields；内部:n8n-workflow；本地:../createVectorStoreNode/createVectorStoreNode、../methods/listSearch、../shared/descriptions。导出:VectorStorePinecone。关键函数/方法:getVectorStoreClient、populateVectorStore、indexes。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStorePinecone/VectorStorePinecone.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStorePinecone/VectorStorePinecone_node.py

import type { PineconeStoreParams } from '@langchain/pinecone';
import { PineconeStore } from '@langchain/pinecone';
import { Pinecone } from '@pinecone-database/pinecone';
import { NodeOperationError, type INodeProperties } from 'n8n-workflow';

import { metadataFilterField } from '@utils/sharedFields';

import { createVectorStoreNode } from '../shared/createVectorStoreNode/createVectorStoreNode';
import { pineconeIndexSearch } from '../shared/createVectorStoreNode/methods/listSearch';
import { pineconeIndexRLC } from '../shared/descriptions';

const sharedFields: INodeProperties[] = [pineconeIndexRLC];

const pineconeNamespaceField: INodeProperties = {
	displayName: 'Pinecone Namespace',
	name: 'pineconeNamespace',
	type: 'string',
	description:
		'Partition the records in an index into namespaces. Queries and other operations are then limited to one namespace, so different requests can search different subsets of your index.',
	default: '',
};

const retrieveFields: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [pineconeNamespaceField, metadataFilterField],
	},
];

const insertFields: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [
			{
				displayName: 'Clear Namespace',
				name: 'clearNamespace',
				type: 'boolean',
				default: false,
				description: 'Whether to clear the namespace before inserting new data',
			},
			pineconeNamespaceField,
		],
	},
];

export class VectorStorePinecone extends createVectorStoreNode<PineconeStore>({
	meta: {
		displayName: 'Pinecone Vector Store',
		name: 'vectorStorePinecone',
		description: 'Work with your data in Pinecone Vector Store',
		icon: { light: 'file:pinecone.svg', dark: 'file:pinecone.dark.svg' },
		docsUrl:
			'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstorepinecone/',
		credentials: [
			{
				name: 'pineconeApi',
				required: true,
			},
		],
		operationModes: ['load', 'insert', 'retrieve', 'update', 'retrieve-as-tool'],
	},
	methods: { listSearch: { pineconeIndexSearch } },
	retrieveFields,
	loadFields: retrieveFields,
	insertFields,
	sharedFields,
	async getVectorStoreClient(context, filter, embeddings, itemIndex) {
		const index = context.getNodeParameter('pineconeIndex', itemIndex, '', {
			extractValue: true,
		}) as string;
		const options = context.getNodeParameter('options', itemIndex, {}) as {
			pineconeNamespace?: string;
		};
		const credentials = await context.getCredentials('pineconeApi');

		const client = new Pinecone({
			apiKey: credentials.apiKey as string,
		});

		const pineconeIndex = client.Index(index);
		const config: PineconeStoreParams = {
			namespace: options.pineconeNamespace ?? undefined,
			pineconeIndex,
			filter,
		};

		return await PineconeStore.fromExistingIndex(embeddings, config);
	},
	async populateVectorStore(context, embeddings, documents, itemIndex) {
		const index = context.getNodeParameter('pineconeIndex', itemIndex, '', {
			extractValue: true,
		}) as string;
		const options = context.getNodeParameter('options', itemIndex, {}) as {
			pineconeNamespace?: string;
			clearNamespace?: boolean;
		};
		const credentials = await context.getCredentials('pineconeApi');

		const client = new Pinecone({
			apiKey: credentials.apiKey as string,
		});

		const indexes = ((await client.listIndexes()).indexes ?? []).map((i) => i.name);

		if (!indexes.includes(index)) {
			throw new NodeOperationError(context.getNode(), `Index ${index} not found`, {
				itemIndex,
				description: 'Please check that the index exists in your vector store',
			});
		}

		const pineconeIndex = client.Index(index);

		if (options.pineconeNamespace && options.clearNamespace) {
			const namespace = pineconeIndex.namespace(options.pineconeNamespace);
			try {
				await namespace.deleteAll();
			} catch (error) {
				// Namespace doesn't exist yet
				context.logger.info(`Namespace ${options.pineconeNamespace} does not exist yet`);
			}
		}

		await PineconeStore.fromDocuments(documents, embeddings, {
			namespace: options.pineconeNamespace ?? undefined,
			pineconeIndex,
		});
	},
}) {}
