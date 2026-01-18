"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/document_loaders/DocumentBinaryInputLoader/DocumentBinaryInputLoader.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/document_loaders/DocumentBinaryInputLoader 的节点。导入/依赖:外部:@langchain/textsplitters、@utils/logWrapper、@utils/N8nBinaryLoader、@utils/sharedFields；内部:无；本地:无。导出:DocumentBinaryInputLoader。关键函数/方法:getConnectionHintNoticeField、supplyData、textSplitter。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/document_loaders/DocumentBinaryInputLoader/DocumentBinaryInputLoader.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/document_loaders/DocumentBinaryInputLoader/DocumentBinaryInputLoader_node.py

import type { TextSplitter } from '@langchain/textsplitters';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { N8nBinaryLoader } from '@utils/N8nBinaryLoader';
import { getConnectionHintNoticeField, metadataFilterField } from '@utils/sharedFields';

// Dependencies needed underneath the hood for the loaders. We add them
// here only to track where what dependency is sued
// import 'd3-dsv'; // for csv
import 'mammoth'; // for docx
import 'epub2'; // for epub
import 'pdf-parse'; // for pdf

export class DocumentBinaryInputLoader implements INodeType {
	description: INodeTypeDescription = {
		// This node is deprecated and will be removed in the future.
		// The functionality was merged with the `DocumentJSONInputLoader` to `DocumentDefaultDataLoader`
		hidden: true,
		displayName: 'Binary Input Loader',
		name: 'documentBinaryInputLoader',
		icon: 'file:binary.svg',
		group: ['transform'],
		version: 1,
		description: 'Use binary data from a previous step in the workflow',
		defaults: {
			name: 'Binary Input Loader',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Document Loaders'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.documentdefaultdataloader/',
					},
				],
			},
		},

		inputs: [
			{
				displayName: 'Text Splitter',
				maxConnections: 1,
				type: NodeConnectionTypes.AiTextSplitter,
				required: true,
			},
		],

		outputs: [NodeConnectionTypes.AiDocument],
		outputNames: ['Document'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiVectorStore]),
			{
				displayName: 'Loader Type',
				name: 'loader',
				type: 'options',
				default: 'jsonLoader',
				required: true,
				options: [
					{
						name: 'CSV Loader',
						value: 'csvLoader',
						description: 'Load CSV files',
					},
					{
						name: 'Docx Loader',
						value: 'docxLoader',
						description: 'Load Docx documents',
					},
					{
						name: 'EPub Loader',
						value: 'epubLoader',
						description: 'Load EPub files',
					},
					{
						name: 'JSON Loader',
						value: 'jsonLoader',
						description: 'Load JSON files',
					},
					{
						name: 'PDF Loader',
						value: 'pdfLoader',
						description: 'Load PDF documents',
					},
					{
						name: 'Text Loader',
						value: 'textLoader',
						description: 'Load plain text files',
					},
				],
			},
			{
				displayName: 'Binary Data Key',
				name: 'binaryDataKey',
				type: 'string',
				default: 'data',
				required: true,
				description: 'Name of the binary property from which to read the file buffer',
			},
			// PDF Only Fields
			{
				displayName: 'Split Pages',
				name: 'splitPages',
				type: 'boolean',
				default: true,
				displayOptions: {
					show: {
						loader: ['pdfLoader'],
					},
				},
			},
			// CSV Only Fields
			{
				displayName: 'Column',
				name: 'column',
				type: 'string',
				default: '',
				description: 'Column to extract from CSV',
				displayOptions: {
					show: {
						loader: ['csvLoader'],
					},
				},
			},
			{
				displayName: 'Separator',
				name: 'separator',
				type: 'string',
				description: 'Separator to use for CSV',
				default: ',',
				displayOptions: {
					show: {
						loader: ['csvLoader'],
					},
				},
			},
			// JSON Only Fields
			{
				displayName: 'Pointers',
				name: 'pointers',
				type: 'string',
				default: '',
				description: 'Pointers to extract from JSON, e.g. "/text" or "/text, /meta/title"',
				displayOptions: {
					show: {
						loader: ['jsonLoader'],
					},
				},
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add Option',
				default: {},
				options: [
					{
						...metadataFilterField,
						displayName: 'Metadata',
						description:
							'Metadata to add to each document. Could be used for filtering during retrieval',
						placeholder: 'Add property',
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions): Promise<SupplyData> {
		this.logger.debug('Supply Data for Binary Input Loader');
		const textSplitter = (await this.getInputConnectionData(
			NodeConnectionTypes.AiTextSplitter,
			0,
		)) as TextSplitter | undefined;

		const binaryDataKey = this.getNodeParameter('binaryDataKey', 0) as string;
		const processor = new N8nBinaryLoader(this, undefined, binaryDataKey, textSplitter);

		return {
			response: logWrapper(processor, this),
		};
	}
}
