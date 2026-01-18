"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverMultiQuery/RetrieverMultiQuery.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverMultiQuery 的节点。导入/依赖:外部:@langchain/core/…/base、@langchain/core/retrievers、@langchain/classic/…/multi_query、@utils/logWrapper；内部:无；本地:无。导出:RetrieverMultiQuery。关键函数/方法:supplyData、model、baseRetriever。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverMultiQuery/RetrieverMultiQuery.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/retrievers/RetrieverMultiQuery/RetrieverMultiQuery_node.py

import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import type { BaseRetriever } from '@langchain/core/retrievers';
import { MultiQueryRetriever } from '@langchain/classic/retrievers/multi_query';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';

export class RetrieverMultiQuery implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'MultiQuery Retriever',
		name: 'retrieverMultiQuery',
		icon: 'fa:box-open',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description:
			'Automates prompt tuning, generates diverse queries and expands document pool for enhanced retrieval.',
		defaults: {
			name: 'MultiQuery Retriever',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Retrievers'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.retrievermultiquery/',
					},
				],
			},
		},

		inputs: [
			{
				displayName: 'Model',
				maxConnections: 1,
				type: NodeConnectionTypes.AiLanguageModel,
				required: true,
			},
			{
				displayName: 'Retriever',
				maxConnections: 1,
				type: NodeConnectionTypes.AiRetriever,
				required: true,
			},
		],
		outputs: [
			{
				displayName: 'Retriever',
				maxConnections: 1,
				type: NodeConnectionTypes.AiRetriever,
			},
		],
		properties: [
			{
				displayName: 'Options',
				name: 'options',
				placeholder: 'Add Option',
				description: 'Additional options to add',
				type: 'collection',
				default: {},
				options: [
					{
						displayName: 'Query Count',
						name: 'queryCount',
						default: 3,
						typeOptions: { minValue: 1 },
						description: 'Number of different versions of the given question to generate',
						type: 'number',
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supplying data for MultiQuery Retriever');

		const options = this.getNodeParameter('options', itemIndex, {}) as { queryCount?: number };

		const model = (await this.getInputConnectionData(
			NodeConnectionTypes.AiLanguageModel,
			itemIndex,
		)) as BaseLanguageModel;

		const baseRetriever = (await this.getInputConnectionData(
			NodeConnectionTypes.AiRetriever,
			itemIndex,
		)) as BaseRetriever;

		// TODO: Add support for parserKey

		const retriever = MultiQueryRetriever.fromLLM({
			llm: model,
			retriever: baseRetriever,
			...options,
		});

		return {
			response: logWrapper(retriever, this),
		};
	}
}
