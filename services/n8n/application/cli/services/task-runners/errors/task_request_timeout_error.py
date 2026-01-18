"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/task-request-timeout.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:TaskRequestTimeoutError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/task-request-timeout.error.ts -> services/n8n/application/cli/services/task-runners/errors/task_request_timeout_error.py

import { OperationalError } from 'n8n-workflow';

export class TaskRequestTimeoutError extends OperationalError {
	description: string;

	constructor({ timeout, isSelfHosted }: { timeout: number; isSelfHosted: boolean }) {
		super(`Task request timed out after ${timeout} ${timeout === 1 ? 'second' : 'seconds'}`);

		const description = [
			'Your Code node task was not matched to a runner within the timeout period. This indicates that the task runner is currently down, or not ready, or at capacity, so it cannot service your task.',
			'If you are repeatedly executing Code nodes with long-running tasks across your instance, please space them apart to give the runner time to catch up. If this does not describe your use case, please open a GitHub issue or reach out to support.',
		];

		if (isSelfHosted) {
			description.push(
				'If needed, you can increase the timeout using the N8N_RUNNERS_TASK_REQUEST_TIMEOUT environment variable.',
			);
		}

		this.description = description.join('<br/><br/>');
	}
}
