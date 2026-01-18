"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/N8nJsonLoader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils 的工具。导入/依赖:外部:@langchain/core/documents、@langchain/textsplitters、@langchain/classic/…/json、@langchain/classic/…/text；内部:无；本地:./helpers。导出:N8nJsonLoader。关键函数/方法:processAll、processItem。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/N8nJsonLoader.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/N8nJsonLoader.py

import type { Document } from '@langchain/core/documents';
import type { TextSplitter } from '@langchain/textsplitters';
import { JSONLoader } from '@langchain/classic/document_loaders/fs/json';
import { TextLoader } from '@langchain/classic/document_loaders/fs/text';
import {
	type IExecuteFunctions,
	type INodeExecutionData,
	type ISupplyDataFunctions,
	NodeOperationError,
} from 'n8n-workflow';

import { getMetadataFiltersValues } from './helpers';

export class N8nJsonLoader {
	constructor(
		private context: IExecuteFunctions | ISupplyDataFunctions,
		private optionsPrefix = '',
		private textSplitter?: TextSplitter,
	) {}

	async processAll(items?: INodeExecutionData[]): Promise<Document[]> {
		const docs: Document[] = [];

		if (!items) return [];

		for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
			const processedDocuments = await this.processItem(items[itemIndex], itemIndex);

			docs.push(...processedDocuments);
		}

		return docs;
	}

	async processItem(item: INodeExecutionData, itemIndex: number): Promise<Document[]> {
		const mode = this.context.getNodeParameter('jsonMode', itemIndex, 'allInputData') as
			| 'allInputData'
			| 'expressionData';

		const pointers = this.context.getNodeParameter(
			`${this.optionsPrefix}pointers`,
			itemIndex,
			'',
		) as string;
		const pointersArray = pointers.split(',').map((pointer) => pointer.trim());
		const metadata = getMetadataFiltersValues(this.context, itemIndex) ?? [];

		if (!item) return [];

		let documentLoader: JSONLoader | TextLoader | null = null;

		if (mode === 'allInputData') {
			const itemString = JSON.stringify(item.json);
			const itemBlob = new Blob([itemString], { type: 'application/json' });
			documentLoader = new JSONLoader(itemBlob, pointersArray);
		}

		if (mode === 'expressionData') {
			const dataString = this.context.getNodeParameter('jsonData', itemIndex) as string | object;
			if (typeof dataString === 'object') {
				const itemBlob = new Blob([JSON.stringify(dataString)], { type: 'application/json' });
				documentLoader = new JSONLoader(itemBlob, pointersArray);
			}

			if (typeof dataString === 'string') {
				const itemBlob = new Blob([dataString], { type: 'text/plain' });
				documentLoader = new TextLoader(itemBlob);
			}
		}

		if (documentLoader === null) {
			// This should never happen
			throw new NodeOperationError(this.context.getNode(), 'Document loader is not initialized');
		}

		const docs = this.textSplitter
			? await this.textSplitter.splitDocuments(await documentLoader.load())
			: await documentLoader.load();

		if (metadata) {
			docs.forEach((doc) => {
				doc.metadata = {
					...doc.metadata,
					...metadata,
				};
			});
		}
		return docs;
	}
}
