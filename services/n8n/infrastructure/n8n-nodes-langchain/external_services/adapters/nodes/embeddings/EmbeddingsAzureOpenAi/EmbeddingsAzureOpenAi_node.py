"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsAzureOpenAi/EmbeddingsAzureOpenAi.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsAzureOpenAi 的节点。导入/依赖:外部:@langchain/openai、@utils/httpProxyAgent、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:EmbeddingsAzureOpenAi。关键函数/方法:getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/embeddings/EmbeddingsAzureOpenAi/EmbeddingsAzureOpenAi.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/embeddings/EmbeddingsAzureOpenAi/EmbeddingsAzureOpenAi_node.py

import { AzureOpenAIEmbeddings } from '@langchain/openai';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { getProxyAgent } from '@utils/httpProxyAgent';
import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

export class EmbeddingsAzureOpenAi implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Embeddings Azure OpenAI',
		name: 'embeddingsAzureOpenAi',
		icon: 'file:azure.svg',
		credentials: [
			{
				name: 'azureOpenAiApi',
				required: true,
			},
		],
		group: ['transform'],
		version: 1,
		description: 'Use Embeddings Azure OpenAI',
		defaults: {
			name: 'Embeddings Azure OpenAI',
		},

		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Embeddings'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.embeddingsazureopenai/',
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
				displayName: 'Model (Deployment) Name',
				name: 'model',
				type: 'string',
				description: 'The name of the model(deployment) to use',
				default: '',
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
					{
						displayName: 'Timeout',
						name: 'timeout',
						default: -1,
						description:
							'Maximum amount of time a request is allowed to take in seconds. Set to -1 for no timeout.',
						type: 'number',
					},
					{
						displayName: 'Dimensions',
						name: 'dimensions',
						default: undefined,
						description:
							'The number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models.',
						type: 'options',
						options: [
							{
								name: '256',
								value: 256,
							},
							{
								name: '512',
								value: 512,
							},
							{
								name: '1024',
								value: 1024,
							},
							{
								name: '1536',
								value: 1536,
							},
							{
								name: '3072',
								value: 3072,
							},
						],
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply data for embeddings');
		const credentials = await this.getCredentials<{
			apiKey: string;
			resourceName: string;
			apiVersion: string;
			endpoint?: string;
		}>('azureOpenAiApi');
		const modelName = this.getNodeParameter('model', itemIndex) as string;

		const options = this.getNodeParameter('options', itemIndex, {}) as {
			batchSize?: number;
			stripNewLines?: boolean;
			timeout?: number;
			dimensions?: number | undefined;
		};

		if (options.timeout === -1) {
			options.timeout = undefined;
		}

		const embeddings = new AzureOpenAIEmbeddings({
			azureOpenAIApiDeploymentName: modelName,
			// instance name only needed to set base url
			azureOpenAIApiInstanceName: !credentials.endpoint ? credentials.resourceName : undefined,
			azureOpenAIApiKey: credentials.apiKey,
			azureOpenAIApiVersion: credentials.apiVersion,
			// azureOpenAIEndpoint and configuration.baseURL are both ignored here
			// only setting azureOpenAIBasePath worked
			azureOpenAIBasePath: credentials.endpoint
				? `${credentials.endpoint}/openai/deployments`
				: undefined,
			configuration: {
				fetchOptions: {
					dispatcher: getProxyAgent(
						credentials.endpoint ?? `https://${credentials.resourceName}.openai.azure.com`,
					),
				},
			},
			...options,
		});

		return {
			response: logWrapper(embeddings, this),
		};
	}
}
