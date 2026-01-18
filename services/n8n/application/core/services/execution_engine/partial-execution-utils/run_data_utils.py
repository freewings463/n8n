"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/run-data-utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getNextExecutionIndex。关键函数/方法:getNextExecutionIndex。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/run-data-utils.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/run_data_utils.py

import type { IRunData } from 'n8n-workflow';

/**
 * Calculates the next execution index by finding the highest existing index in the run data and incrementing by 1.
 *
 * The execution index is used to track the sequence of workflow executions.
 *
 * @param {IRunData} [runData={}]
 * @returns {number} The next execution index (previous highest index + 1, or 0 if no previous executionIndex exist).
 */
export function getNextExecutionIndex(runData: IRunData = {}): number {
	// If runData is empty, return 0 as the first execution index
	if (!runData || Object.keys(runData).length === 0) return 0;

	const previousIndices = Object.values(runData)
		.flat()
		.map((taskData) => taskData.executionIndex)
		// filter out undefined if previous execution does not have index
		// this can happen if rerunning execution before executionIndex was introduced
		.filter((value) => typeof value === 'number');

	// If no valid indices were found, return 0 as the first execution index
	if (previousIndices.length === 0) return 0;

	return Math.max(...previousIndices) + 1;
}
