"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/n8nDefaultFailedAttemptHandler.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:n8nDefaultFailedAttemptHandler。关键函数/方法:n8nDefaultFailedAttemptHandler。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/n8nDefaultFailedAttemptHandler.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/n8nDefaultFailedAttemptHandler.py

const STATUS_NO_RETRY = [
	400, // Bad Request
	401, // Unauthorized
	402, // Payment Required
	403, // Forbidden
	404, // Not Found
	405, // Method Not Allowed
	406, // Not Acceptable
	407, // Proxy Authentication Required
	409, // Conflict
];

/**
 * This function is used as a default handler for failed attempts in all LLMs.
 * It is based on a default handler from the langchain core package.
 * It throws an error when it encounters a known error that should not be retried.
 * @param error
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const n8nDefaultFailedAttemptHandler = (error: any) => {
	if (
		// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access,@typescript-eslint/no-unsafe-call
		error?.message?.startsWith?.('Cancel') ||
		error?.message?.startsWith?.('AbortError') ||
		error?.name === 'AbortError'
	) {
		throw error;
	}

	// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
	if (error?.code === 'ECONNABORTED') {
		throw error;
	}

	const status =
		// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
		error?.response?.status ?? error?.status;
	if (status && STATUS_NO_RETRY.includes(+status)) {
		throw error;
	}
};
