"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterTokenSplitter/TextSplitterTokenSplitter.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterTokenSplitter 的节点。导入/依赖:外部:@utils/logWrapper、@utils/sharedFields；内部:无；本地:./TokenTextSplitter。导出:TextSplitterTokenSplitter。关键函数/方法:getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterTokenSplitter/TextSplitterTokenSplitter.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/text_splitters/TextSplitterTokenSplitter/TextSplitterTokenSplitter_node.py

import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

import { TokenTextSplitter } from './TokenTextSplitter';

export class TextSplitterTokenSplitter implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Token Splitter',
		name: 'textSplitterTokenSplitter',
		icon: 'fa:grip-lines-vertical',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description: 'Split text into chunks by tokens',
		defaults: {
			name: 'Token Splitter',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Text Splitters'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.textsplittertokensplitter/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiTextSplitter],
		outputNames: ['Text Splitter'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiDocument]),
			{
				displayName: 'Chunk Size',
				name: 'chunkSize',
				type: 'number',
				default: 1000,
				description: 'Maximum number of tokens per chunk',
			},
			{
				displayName: 'Chunk Overlap',
				name: 'chunkOverlap',
				type: 'number',
				default: 0,
				description: 'Number of tokens shared between consecutive chunks to preserve context',
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply Data for Text Splitter');

		const chunkSize = this.getNodeParameter('chunkSize', itemIndex) as number;
		const chunkOverlap = this.getNodeParameter('chunkOverlap', itemIndex) as number;

		const splitter = new TokenTextSplitter({
			chunkSize,
			chunkOverlap,
			allowedSpecial: 'all',
			disallowedSpecial: 'all',
			encodingName: 'cl100k_base',
			keepSeparator: false,
		});

		return {
			response: logWrapper(splitter, this),
		};
	}
}
