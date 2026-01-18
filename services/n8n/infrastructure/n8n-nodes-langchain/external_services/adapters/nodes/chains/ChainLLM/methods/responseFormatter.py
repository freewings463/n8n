"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainLLM/methods/responseFormatter.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainLLM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:formatResponse。关键函数/方法:formatResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainLLM/methods/responseFormatter.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainLLM/methods/responseFormatter.py

import type { IDataObject } from 'n8n-workflow';

/**
 * Formats the response from the LLM chain into a consistent structure
 */
export function formatResponse(response: unknown, returnUnwrappedObject: boolean): IDataObject {
	if (typeof response === 'string') {
		return {
			text: response.trim(),
		};
	}

	if (Array.isArray(response)) {
		return {
			data: response,
		};
	}

	if (response instanceof Object) {
		if (returnUnwrappedObject) {
			return response as IDataObject;
		}

		// If the response is an object and we are not unwrapping it, we need to stringify it
		// to be backwards compatible with older versions of the chain(< 1.6)
		return {
			text: JSON.stringify(response),
		};
	}

	return {
		response: {
			text: response,
		},
	};
}
