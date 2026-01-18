"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/n8nLlmFailedAttemptHandler.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms 的节点。导入/依赖:外部:@langchain/core/…/async_caller；内部:n8n-workflow；本地:./n8nDefaultFailedAttemptHandler。导出:makeN8nLlmFailedAttemptHandler。关键函数/方法:makeN8nLlmFailedAttemptHandler、n8nDefaultFailedAttemptHandler。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/n8nLlmFailedAttemptHandler.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/n8nLlmFailedAttemptHandler.py

import type { FailedAttemptHandler } from '@langchain/core/dist/utils/async_caller';
import type { ISupplyDataFunctions, JsonObject } from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import { n8nDefaultFailedAttemptHandler } from './n8nDefaultFailedAttemptHandler';

/**
 * This function returns a custom failed attempt handler for using with LangChain models.
 * It first tries to use a custom handler passed as an argument, and if that doesn't throw an error, it uses the default handler.
 * It always wraps the error in a NodeApiError.
 * It throws an error ONLY if there are no retries left.
 */
export const makeN8nLlmFailedAttemptHandler = (
	ctx: ISupplyDataFunctions,
	handler?: FailedAttemptHandler,
): FailedAttemptHandler => {
	return (error: any) => {
		try {
			// Try custom error handler first
			handler?.(error);

			// If it didn't throw an error, use the default handler
			n8nDefaultFailedAttemptHandler(error);
		} catch (e) {
			// Wrap the error in a NodeApiError
			const apiError = new NodeApiError(ctx.getNode(), e as unknown as JsonObject, {
				functionality: 'configuration-node',
			});

			throw apiError;
		}

		// If no error was thrown, check if it is the last retry
		// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
		if (error?.retriesLeft > 0) {
			return;
		}

		// If there are no retries left, throw the error wrapped in a NodeApiError
		const apiError = new NodeApiError(ctx.getNode(), error as unknown as JsonObject, {
			functionality: 'configuration-node',
		});

		throw apiError;
	};
};
