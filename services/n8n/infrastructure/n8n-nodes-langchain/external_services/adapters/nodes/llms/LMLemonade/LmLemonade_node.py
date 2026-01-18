"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LMLemonade/LmLemonade.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LMLemonade 的节点。导入/依赖:外部:@langchain/openai、@utils/sharedFields；内部:无；本地:../credentials/LemonadeApi.credentials、./description、../n8nLlmFailedAttemptHandler、../N8nLlmTracing。导出:LmLemonade。关键函数/方法:getConnectionHintNoticeField、supplyData、credentials。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LMLemonade/LmLemonade.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LMLemonade/LmLemonade_node.py

import { OpenAI } from '@langchain/openai';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import type { LemonadeApiCredentialsType } from '../../../credentials/LemonadeApi.credentials';

import { getConnectionHintNoticeField } from '@utils/sharedFields';

import { lemonadeDescription, lemonadeModel, lemonadeOptions } from './description';
import { makeN8nLlmFailedAttemptHandler } from '../n8nLlmFailedAttemptHandler';
import { N8nLlmTracing } from '../N8nLlmTracing';

export class LmLemonade implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Lemonade Model',

		name: 'lmLemonade',
		icon: 'file:lemonade.svg',
		group: ['transform'],
		version: 1,
		description: 'Language Model Lemonade',
		defaults: {
			name: 'Lemonade Model',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Language Models', 'Root Nodes'],
				'Language Models': ['Text Completion Models'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmlemonade/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiLanguageModel],
		outputNames: ['Model'],
		...lemonadeDescription,
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiChain, NodeConnectionTypes.AiAgent]),
			lemonadeModel,
			lemonadeOptions,
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const credentials = (await this.getCredentials('lemonadeApi')) as LemonadeApiCredentialsType;

		const modelName = this.getNodeParameter('model', itemIndex) as string;
		const options = this.getNodeParameter('options', itemIndex, {}) as {
			temperature?: number;
			topP?: number;
			frequencyPenalty?: number;
			presencePenalty?: number;
			maxTokens?: number;
			stop?: string;
		};

		// Process stop sequences
		let stop: string[] | undefined;
		if (options.stop) {
			const stopSequences = options.stop
				.split(',')
				.map((s) => s.trim())
				.filter((s) => s.length > 0);
			stop = stopSequences.length > 0 ? stopSequences : undefined;
		}

		// Ensure we have an API key for OpenAI client validation
		const apiKey = credentials.apiKey || 'lemonade-placeholder-key';

		// Build configuration object separately like official OpenAI node
		const configuration: any = {
			baseURL: credentials.baseUrl,
		};

		// Add custom headers if API key is provided
		if (credentials.apiKey) {
			configuration.defaultHeaders = {
				Authorization: `Bearer ${credentials.apiKey}`,
			};
		}

		const model = new OpenAI({
			apiKey,
			model: modelName,
			temperature: options.temperature,
			topP: options.topP,
			frequencyPenalty: options.frequencyPenalty,
			presencePenalty: options.presencePenalty,
			maxTokens: options.maxTokens && options.maxTokens > 0 ? options.maxTokens : undefined,
			stop,
			configuration,
			callbacks: [new N8nLlmTracing(this)],
			onFailedAttempt: makeN8nLlmFailedAttemptHandler(this),
		});

		return {
			response: model,
		};
	}
}
