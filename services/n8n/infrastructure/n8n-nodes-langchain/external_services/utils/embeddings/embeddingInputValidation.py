"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/embeddings/embeddingInputValidation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/embeddings 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateEmbedQueryInput、validateEmbedDocumentsInput。关键函数/方法:validateEmbedQueryInput、validateEmbedDocumentsInput。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/embeddings/embeddingInputValidation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/embeddings/embeddingInputValidation.py

import type { INode } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

/**
 * Validates query input for embedQuery operations.
 * Throws NodeOperationError if query is invalid (undefined, null, or empty string).
 *
 * @param query - The query to validate
 * @param node - The node for error context
 * @returns The validated query string
 * @throws NodeOperationError if query is invalid
 */
export function validateEmbedQueryInput(query: unknown, node: INode): string {
	if (typeof query !== 'string' || query === '') {
		throw new NodeOperationError(node, 'Cannot embed empty or undefined text', {
			description:
				'The text provided for embedding is empty or undefined. This can happen when: the input expression evaluates to undefined, the AI agent calls a tool without proper arguments, or a required field is missing.',
		});
	}
	return query;
}

/**
 * Validates documents input for embedDocuments operations.
 * Throws NodeOperationError if documents array is invalid or contains invalid entries.
 *
 * @param documents - The documents array to validate
 * @param node - The node for error context
 * @returns The validated documents array
 * @throws NodeOperationError if documents is not an array or contains invalid entries
 */
export function validateEmbedDocumentsInput(documents: unknown, node: INode): string[] {
	if (!Array.isArray(documents)) {
		throw new NodeOperationError(node, 'Documents must be an array', {
			description: 'Expected an array of strings to embed.',
		});
	}

	const invalidIndex = documents.findIndex(
		(doc) => doc === undefined || doc === null || doc === '',
	);

	if (invalidIndex !== -1) {
		throw new NodeOperationError(node, `Invalid document at index ${invalidIndex}`, {
			description: `Document at index ${invalidIndex} is empty or undefined. All documents must be non-empty strings.`,
		});
	}

	return documents;
}
