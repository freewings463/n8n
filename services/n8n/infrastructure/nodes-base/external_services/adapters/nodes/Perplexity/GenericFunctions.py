"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Perplexity/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Perplexity 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:sendErrorPostReceive、error。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Perplexity/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Perplexity/GenericFunctions.py

import type {
	IExecuteSingleFunctions,
	IN8nHttpFullResponse,
	INodeExecutionData,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function sendErrorPostReceive(
	this: IExecuteSingleFunctions,
	data: INodeExecutionData[],
	response: IN8nHttpFullResponse,
): Promise<INodeExecutionData[]> {
	if (String(response.statusCode).startsWith('4') || String(response.statusCode).startsWith('5')) {
		const errorBody = response.body as JsonObject;
		const error = (errorBody?.error ?? {}) as JsonObject;

		const errorMessage =
			typeof error.message === 'string'
				? error.message
				: (response.statusMessage ?? 'An unexpected issue occurred');
		const errorType = typeof error.type === 'string' ? error.type : 'UnknownError';
		const itemIndex = typeof error.itemIndex === 'number' ? `[Item ${error.itemIndex}]` : '';

		if (errorType === 'invalid_model') {
			throw new NodeApiError(this.getNode(), errorBody, {
				message: 'Invalid model',
				description:
					'The model is not valid. Permitted models can be found in the documentation at https://docs.perplexity.ai/guides/model-cards.',
			});
		}

		// Fallback for other errors
		throw new NodeApiError(this.getNode(), response as unknown as JsonObject, {
			message: `${errorMessage}${itemIndex ? ' ' + itemIndex : ''}.`,
			description:
				'Any optional system messages must be sent first, followed by alternating user and assistant messages. For more details, refer to the API documentation: https://docs.perplexity.ai/api-reference/chat-completions',
		});
	}
	return data;
}
