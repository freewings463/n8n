"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/document_loaders/DocumentJSONInputLoader/DocumentJsonInputLoader.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/document_loaders/DocumentJSONInputLoader 的节点。导入/依赖:外部:@langchain/textsplitters、@utils/logWrapper、@utils/N8nJsonLoader、@utils/sharedFields；内部:无；本地:无。导出:DocumentJsonInputLoader。关键函数/方法:getConnectionHintNoticeField、supplyData、textSplitter。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/document_loaders/DocumentJSONInputLoader/DocumentJsonInputLoader.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/document_loaders/DocumentJSONInputLoader/DocumentJsonInputLoader_node.py

import type { TextSplitter } from '@langchain/textsplitters';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { N8nJsonLoader } from '@utils/N8nJsonLoader';
import { getConnectionHintNoticeField, metadataFilterField } from '@utils/sharedFields';

export class DocumentJsonInputLoader implements INodeType {
	description: INodeTypeDescription = {
		// This node is deprecated and will be removed in the future.
		// The functionality was merged with the `DocumentBinaryInputLoader` to `DocumentDefaultDataLoader`
		hidden: true,
		displayName: 'JSON Input Loader',
		name: 'documentJsonInputLoader',
		icon: 'file:json.svg',
		group: ['transform'],
		version: 1,
		description: 'Use JSON data from a previous step in the workflow',
		defaults: {
			name: 'JSON Input Loader',
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
			},
		],
		inputNames: ['Text Splitter'],

		outputs: [NodeConnectionTypes.AiDocument],
		outputNames: ['Document'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiVectorStore]),
			{
				displayName: 'Pointers',
				name: 'pointers',
				type: 'string',
				default: '',
				description: 'Pointers to extract from JSON, e.g. "/text" or "/text, /meta/title"',
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
		this.logger.debug('Supply Data for JSON Input Loader');
		const textSplitter = (await this.getInputConnectionData(
			NodeConnectionTypes.AiTextSplitter,
			0,
		)) as TextSplitter | undefined;

		const processor = new N8nJsonLoader(this, undefined, textSplitter);

		return {
			response: logWrapper(processor, this),
		};
	}
}
