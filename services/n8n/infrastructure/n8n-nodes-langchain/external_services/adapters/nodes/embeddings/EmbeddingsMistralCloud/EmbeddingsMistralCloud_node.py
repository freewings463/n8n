"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsMistralCloud/EmbeddingsMistralCloud.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsMistralCloud 的节点。导入/依赖:外部:@langchain/mistralai、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:EmbeddingsMistralCloud。关键函数/方法:getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsMistralCloud/EmbeddingsMistralCloud.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/embeddings/EmbeddingsMistralCloud/EmbeddingsMistralCloud_node.py

import type { MistralAIEmbeddingsParams } from '@langchain/mistralai';
import { MistralAIEmbeddings } from '@langchain/mistralai';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

export class EmbeddingsMistralCloud implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Embeddings Mistral Cloud',
		name: 'embeddingsMistralCloud',
		icon: 'file:mistral.svg',
		credentials: [
			{
				name: 'mistralCloudApi',
				required: true,
			},
		],
		group: ['transform'],
		version: 1,
		description: 'Use Embeddings Mistral Cloud',
		defaults: {
			name: 'Embeddings Mistral Cloud',
		},

		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Embeddings'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.embeddingsmistralcloud/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiEmbedding],
		outputNames: ['Embeddings'],
		requestDefaults: {
			ignoreHttpStatusErrors: true,
			baseURL: 'https://api.mistral.ai/v1',
		},
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiVectorStore]),
			{
				displayName: 'Model',
				name: 'model',
				type: 'options',
				description:
					'The model which will compute the embeddings. <a href="https://docs.mistral.ai/platform/endpoints/">Learn more</a>.',
				typeOptions: {
					loadOptions: {
						routing: {
							request: {
								method: 'GET',
								url: '/models',
							},
							output: {
								postReceive: [
									{
										type: 'rootProperty',
										properties: {
											property: 'data',
										},
									},
									{
										type: 'filter',
										properties: {
											pass: "={{ $responseItem.id.includes('embed') }}",
										},
									},
									{
										type: 'setKeyValue',
										properties: {
											name: '={{ $responseItem.id }}',
											value: '={{ $responseItem.id }}',
										},
									},
									{
										type: 'sort',
										properties: {
											key: 'name',
										},
									},
								],
							},
						},
					},
				},
				routing: {
					send: {
						type: 'body',
						property: 'model',
					},
				},
				default: 'mistral-embed',
			},
			{
				displayName: 'Options',
				name: 'options',
				placeholder: 'Add Option',
				description: 'Additional options to add',
				type: 'collection',
				default: {},
				options: [
					{
						displayName: 'Batch Size',
						name: 'batchSize',
						default: 512,
						typeOptions: { maxValue: 2048 },
						description: 'Maximum number of documents to send in each request',
						type: 'number',
					},
					{
						displayName: 'Strip New Lines',
						name: 'stripNewLines',
						default: true,
						description: 'Whether to strip new lines from the input text',
						type: 'boolean',
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const credentials = await this.getCredentials('mistralCloudApi');
		const modelName = this.getNodeParameter('model', itemIndex) as string;
		const options = this.getNodeParameter(
			'options',
			itemIndex,
			{},
		) as Partial<MistralAIEmbeddingsParams>;

		const embeddings = new MistralAIEmbeddings({
			apiKey: credentials.apiKey as string,
			model: modelName,
			...options,
		});

		return {
			response: logWrapper(embeddings, this),
		};
	}
}
