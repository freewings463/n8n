"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverContextualCompression/RetrieverContextualCompression.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverContextualCompression 的节点。导入/依赖:外部:@langchain/core/…/base、@langchain/core/retrievers、@langchain/classic/…/contextual_compression、@langchain/classic/…/chain_extract、@utils/logWrapper；内部:无；本地:无。导出:RetrieverContextualCompression。关键函数/方法:supplyData、model、baseRetriever。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/retrievers/RetrieverContextualCompression/RetrieverContextualCompression.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/retrievers/RetrieverContextualCompression/RetrieverContextualCompression_node.py

import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import type { BaseRetriever } from '@langchain/core/retrievers';
import { ContextualCompressionRetriever } from '@langchain/classic/retrievers/contextual_compression';
import { LLMChainExtractor } from '@langchain/classic/retrievers/document_compressors/chain_extract';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';

export class RetrieverContextualCompression implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Contextual Compression Retriever',
		name: 'retrieverContextualCompression',
		icon: 'fa:box-open',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description: 'Enhances document similarity search by contextual compression.',
		defaults: {
			name: 'Contextual Compression Retriever',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Retrievers'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.retrievercontextualcompression/',
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
		properties: [],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supplying data for Contextual Compression Retriever');

		const model = (await this.getInputConnectionData(
			NodeConnectionTypes.AiLanguageModel,
			itemIndex,
		)) as BaseLanguageModel;

		const baseRetriever = (await this.getInputConnectionData(
			NodeConnectionTypes.AiRetriever,
			itemIndex,
		)) as BaseRetriever;

		const baseCompressor = LLMChainExtractor.fromLLM(model);

		const retriever = new ContextualCompressionRetriever({
			baseCompressor,
			baseRetriever,
		});

		return {
			response: logWrapper(retriever, this),
		};
	}
}
