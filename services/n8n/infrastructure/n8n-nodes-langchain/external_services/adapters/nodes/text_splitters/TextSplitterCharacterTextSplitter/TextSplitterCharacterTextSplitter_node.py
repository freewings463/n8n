"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterCharacterTextSplitter/TextSplitterCharacterTextSplitter.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterCharacterTextSplitter 的节点。导入/依赖:外部:@langchain/textsplitters、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:TextSplitterCharacterTextSplitter。关键函数/方法:getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterCharacterTextSplitter/TextSplitterCharacterTextSplitter.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/text_splitters/TextSplitterCharacterTextSplitter/TextSplitterCharacterTextSplitter_node.py

import type { CharacterTextSplitterParams } from '@langchain/textsplitters';
import { CharacterTextSplitter } from '@langchain/textsplitters';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

export class TextSplitterCharacterTextSplitter implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Character Text Splitter',
		name: 'textSplitterCharacterTextSplitter',
		icon: 'fa:grip-lines-vertical',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description: 'Split text into chunks by characters',
		defaults: {
			name: 'Character Text Splitter',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Text Splitters'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.textsplittercharactertextsplitter/',
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
				displayName: 'Separator',
				name: 'separator',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Chunk Size',
				name: 'chunkSize',
				type: 'number',
				default: 1000,
				description: 'Maximum number of characters per chunk',
			},
			{
				displayName: 'Chunk Overlap',
				name: 'chunkOverlap',
				type: 'number',
				default: 0,
				description: 'Number of characters shared between consecutive chunks to preserve context',
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply Data for Text Splitter');

		const separator = this.getNodeParameter('separator', itemIndex) as string;
		const chunkSize = this.getNodeParameter('chunkSize', itemIndex) as number;
		const chunkOverlap = this.getNodeParameter('chunkOverlap', itemIndex) as number;

		const params: CharacterTextSplitterParams = {
			separator,
			chunkSize,
			chunkOverlap,
			keepSeparator: false,
		};

		const splitter = new CharacterTextSplitter(params);

		return {
			response: logWrapper(splitter, this),
		};
	}
}
