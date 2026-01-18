"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterRecursiveCharacterTextSplitter/TextSplitterRecursiveCharacterTextSplitter.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterRecursiveCharacterTextSplitter 的节点。导入/依赖:外部:@langchain/textsplitters、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:TextSplitterRecursiveCharacterTextSplitter。关键函数/方法:getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterRecursiveCharacterTextSplitter/TextSplitterRecursiveCharacterTextSplitter.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/text_splitters/TextSplitterRecursiveCharacterTextSplitter/TextSplitterRecursiveCharacterTextSplitter_node.py

import type {
	RecursiveCharacterTextSplitterParams,
	SupportedTextSplitterLanguage,
} from '@langchain/textsplitters';
import { RecursiveCharacterTextSplitter } from '@langchain/textsplitters';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

const supportedLanguages: SupportedTextSplitterLanguage[] = [
	'cpp',
	'go',
	'java',
	'js',
	'php',
	'proto',
	'python',
	'rst',
	'ruby',
	'rust',
	'scala',
	'swift',
	'markdown',
	'latex',
	'html',
];
export class TextSplitterRecursiveCharacterTextSplitter implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Recursive Character Text Splitter',
		name: 'textSplitterRecursiveCharacterTextSplitter',
		icon: 'fa:grip-lines-vertical',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description: 'Split text into chunks by characters recursively, recommended for most use cases',
		defaults: {
			name: 'Recursive Character Text Splitter',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Text Splitters'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.textsplitterrecursivecharactertextsplitter/',
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
			},
			{
				displayName: 'Chunk Overlap',
				name: 'chunkOverlap',
				type: 'number',
				default: 0,
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
						displayName: 'Split Code',
						name: 'splitCode',
						default: 'markdown',
						type: 'options',
						options: supportedLanguages.map((lang) => ({ name: lang, value: lang })),
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		this.logger.debug('Supply Data for Text Splitter');

		const chunkSize = this.getNodeParameter('chunkSize', itemIndex) as number;
		const chunkOverlap = this.getNodeParameter('chunkOverlap', itemIndex) as number;
		const splitCode = this.getNodeParameter(
			'options.splitCode',
			itemIndex,
			null,
		) as SupportedTextSplitterLanguage | null;
		const params: RecursiveCharacterTextSplitterParams = {
			// TODO: These are the default values, should we allow the user to change them?
			separators: ['\n\n', '\n', ' ', ''],
			chunkSize,
			chunkOverlap,
			keepSeparator: false,
		};
		let splitter: RecursiveCharacterTextSplitter;

		if (splitCode && supportedLanguages.includes(splitCode)) {
			splitter = RecursiveCharacterTextSplitter.fromLanguage(splitCode, params);
		} else {
			splitter = new RecursiveCharacterTextSplitter(params);
		}

		return {
			response: logWrapper(splitter, this),
		};
	}
}
