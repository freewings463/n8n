"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/get-final-test-result.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:../entities、../entities/types-db。导出:getTestRunFinalResult。关键函数/方法:getTestRunFinalResult。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/get-final-test-result.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/get_final_test_result.py

import type { TestCaseExecution } from '../entities';
import type { TestRunFinalResult } from '../entities/types-db';

/**
 * Returns the final result of the test run based on the test case executions.
 * The final result is the most severe status among all test case executions' statuses.
 */
export function getTestRunFinalResult(testCaseExecutions: TestCaseExecution[]): TestRunFinalResult {
	// Priority of statuses: error > warning > success
	const severityMap: Record<TestRunFinalResult, number> = {
		error: 3,
		warning: 2,
		success: 1,
	};

	let finalResult: TestRunFinalResult = 'success';

	for (const testCaseExecution of testCaseExecutions) {
		if (['error', 'warning'].includes(testCaseExecution.status)) {
			if (
				testCaseExecution.status in severityMap &&
				severityMap[testCaseExecution.status as TestRunFinalResult] > severityMap[finalResult]
			) {
				finalResult = testCaseExecution.status as TestRunFinalResult;
			}
		}
	}

	return finalResult;
}
