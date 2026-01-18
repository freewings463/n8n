"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/task-runner-restart-loop-error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:TaskRunnerRestartLoopError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/task-runner-restart-loop-error.ts -> services/n8n/application/cli/services/task-runners/errors/task_runner_restart_loop_error.py

import { UnexpectedError } from 'n8n-workflow';

export class TaskRunnerRestartLoopError extends UnexpectedError {
	constructor(
		readonly howManyTimes: number,
		readonly timePeriodMs: number,
	) {
		const message = `Task runner has restarted ${howManyTimes} times within ${timePeriodMs / 1000} seconds. This is an abnormally high restart rate that suggests a bug or other issue is preventing your runner process from starting up. If this issues persists, please file a report at: https://github.com/n8n-io/n8n/issues`;

		super(message);
	}
}
