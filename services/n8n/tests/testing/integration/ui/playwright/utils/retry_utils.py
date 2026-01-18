"""
MIGRATION-META:
  source_path: packages/testing/playwright/utils/retry-utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:retryUntil。关键函数/方法:retryUntil、tryAgain、setTimeout、resolve、reject。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Retries the given assertion until it passes or the timeout is reached / await retryUntil(。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/utils/retry-utils.ts -> services/n8n/tests/testing/integration/ui/playwright/utils/retry_utils.py

/**
 * Retries the given assertion until it passes or the timeout is reached
 *
 * @example
 * await retryUntil(
 *   () => expect(service.someState).toBe(true)
 * );
 */
export const retryUntil = async (
	assertion: () => Promise<void> | void,
	{ intervalMs = 200, timeoutMs = 5000 } = {},
) => {
	return await new Promise((resolve, reject) => {
		const startTime = Date.now();

		const tryAgain = () => {
			setTimeout(async () => {
				try {
					resolve(await assertion());
				} catch (error) {
					if (Date.now() - startTime > timeoutMs) {
						reject(error instanceof Error ? error : new Error(String(error)));
					} else {
						tryAgain();
					}
				}
			}, intervalMs);
		};

		tryAgain();
	});
};
