"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsHuggingFaceInference/EmbeddingsHuggingFaceInference.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsHuggingFaceInference 的节点。导入/依赖:外部:@huggingface/inference、@langchain/community/…/hf、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:EmbeddingsHuggingFaceInference。关键函数/方法:getConnectionHintNoticeField、supplyData、isValidHFProviderOrPolicy。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsHuggingFaceInference/EmbeddingsHuggingFaceInference.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/embeddings/EmbeddingsHuggingFaceInference/EmbeddingsHuggingFaceInference_node.py

import type { InferenceProviderOrPolicy } from '@huggingface/inference';
import { PROVIDERS_OR_POLICIES } from '@huggingface/inference';
import { HuggingFaceInferenceEmbeddings } from '@langchain/community/embeddings/hf';
import {
	NodeConnectionTypes,
	NodeOperationError,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

export class EmbeddingsHuggingFaceInference implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Embeddings Hugging Face Inference',
		name: 'embeddingsHuggingFaceInference',
		icon: 'file:huggingface.svg',
		group: ['transform'],
		version: 1,
		description: 'Use HuggingFace Inference Embeddings',
		defaults: {
			name: 'Embeddings HuggingFace Inference',
		},
		credentials: [
			{
				name: 'huggingFaceApi',
				required: true,
			},
		],
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Embeddings'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.embeddingshuggingfaceinference/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiEmbedding],
		outputNames: ['Embeddings'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiVectorStore]),
			{
				displayName:
					'Each model is using different dimensional density for embeddings. Please make sure to use the same dimensionality for your vector store. The default model is using 768-dimensional embeddings.',
				name: 'notice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Model Name',
				name: 'modelName',
				type: 'string',
				default: 'sentence-transformers/distilbert-base-nli-mean-tokens',
				description: 'The model name to use from HuggingFace library',
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
						displayName: 'Custom Inference Endpoint',
						name: 'endpointUrl',
						default: '',
						description: 'Custom endpoint URL',
						type: 'string',
					},
					{
						displayName: 'Provider',
						name: 'provider',
						type: 'options',
						options: PROVIDERS_OR_POLICIES.map((value) => ({ value, name: value })),
						default: 'auto',
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply data for embeddings HF Inference');
		const model = this.getNodeParameter(
			'modelName',
			itemIndex,
			'sentence-transformers/distilbert-base-nli-mean-tokens',
		) as string;
		const credentials = await this.getCredentials('huggingFaceApi');
		const options = this.getNodeParameter('options', itemIndex, {}) as object;

		if ('provider' in options && !isValidHFProviderOrPolicy(options.provider)) {
			throw new NodeOperationError(this.getNode(), 'Unsupported provider');
		}

		const embeddings = new HuggingFaceInferenceEmbeddings({
			apiKey: credentials.apiKey as string,
			model,
			...options,
		});

		return {
			response: logWrapper(embeddings, this),
		};
	}
}

function isValidHFProviderOrPolicy(provider: unknown): provider is InferenceProviderOrPolicy {
	return (
		typeof provider === 'string' && (PROVIDERS_OR_POLICIES as readonly string[]).includes(provider)
	);
}
