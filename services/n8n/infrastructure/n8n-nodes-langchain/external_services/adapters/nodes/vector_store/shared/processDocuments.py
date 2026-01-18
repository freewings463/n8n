"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/processDocuments.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的节点。导入/依赖:外部:@langchain/core/documents、@utils/N8nBinaryLoader、@utils/N8nJsonLoader；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:processDocuments、processDocument。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/processDocuments.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/processDocuments.py

import type { Document } from '@langchain/core/documents';
import type { INodeExecutionData } from 'n8n-workflow';

import { N8nBinaryLoader } from '@utils/N8nBinaryLoader';
import { N8nJsonLoader } from '@utils/N8nJsonLoader';

export async function processDocuments(
	documentInput: N8nJsonLoader | N8nBinaryLoader | Array<Document<Record<string, unknown>>>,
	inputItems: INodeExecutionData[],
) {
	let processedDocuments: Document[];

	if (documentInput instanceof N8nJsonLoader || documentInput instanceof N8nBinaryLoader) {
		processedDocuments = await documentInput.processAll(inputItems);
	} else {
		processedDocuments = documentInput;
	}

	const serializedDocuments = processedDocuments.map(({ metadata, pageContent }) => ({
		json: { metadata, pageContent },
	}));

	return {
		processedDocuments,
		serializedDocuments,
	};
}
export async function processDocument(
	documentInput: N8nJsonLoader | N8nBinaryLoader | Array<Document<Record<string, unknown>>>,
	inputItem: INodeExecutionData,
	itemIndex: number,
) {
	let processedDocuments: Document[];

	if (documentInput instanceof N8nJsonLoader || documentInput instanceof N8nBinaryLoader) {
		processedDocuments = await documentInput.processItem(inputItem, itemIndex);
	} else {
		processedDocuments = documentInput;
	}

	const serializedDocuments = processedDocuments.map(({ metadata, pageContent }) => ({
		json: { metadata, pageContent },
		pairedItem: {
			item: itemIndex,
		},
	}));

	return {
		processedDocuments,
		serializedDocuments,
	};
}
