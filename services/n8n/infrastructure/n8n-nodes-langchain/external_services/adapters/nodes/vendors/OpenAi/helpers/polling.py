"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/polling.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/polling.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/polling.py

import type { IExecuteFunctions } from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function pollUntilAvailable<TResponse>(
	ctx: IExecuteFunctions,
	request: () => Promise<TResponse>,
	check: (response: TResponse) => boolean,
	timeoutSeconds: number,
	intervalSeconds = 5,
): Promise<TResponse> {
	const abortSignal = ctx.getExecutionCancelSignal();
	let response: TResponse | undefined;
	const startTime = Date.now();

	while (!response || !check(response)) {
		const elapsedTime = Date.now() - startTime;
		if (elapsedTime >= timeoutSeconds * 1000) {
			throw new NodeApiError(ctx.getNode(), {
				message: 'Timeout reached',
				code: 500,
			});
		}

		if (abortSignal?.aborted) {
			throw new NodeApiError(ctx.getNode(), {
				message: 'Execution was cancelled',
				code: 500,
			});
		}

		response = await request();

		// Wait before the next polling attempt
		await new Promise((resolve) => setTimeout(resolve, intervalSeconds * 1000));
	}

	return response;
}
