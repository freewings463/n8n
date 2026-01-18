"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-broker/errors/task-runner-execution-timeout.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/task-broker/errors 的执行错误。导入/依赖:外部:无；内部:@n8n/config、n8n-workflow；本地:无。导出:TaskRunnerExecutionTimeoutError。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-broker/errors/task-runner-execution-timeout.error.ts -> services/n8n/application/cli/services/task-runners/task-broker/errors/task_runner_execution_timeout_error.py

import type { TaskRunnerMode } from '@n8n/config';
import { OperationalError } from 'n8n-workflow';

export class TaskRunnerExecutionTimeoutError extends OperationalError {
	description: string;

	constructor({
		taskTimeout,
		isSelfHosted,
		mode,
	}: { taskTimeout: number; isSelfHosted: boolean; mode: TaskRunnerMode }) {
		super(
			`Task execution timed out after ${taskTimeout} ${taskTimeout === 1 ? 'second' : 'seconds'}`,
		);

		const subtitles = {
			internal:
				'The task runner was taking too long on this task, so it was suspected of being unresponsive and restarted, and the task was aborted.',
			external: 'The task runner was taking too long on this task, so the task was aborted.',
		};

		const fixes = {
			optimizeScript:
				'Optimize your script to prevent long-running tasks, e.g. by processing data in smaller batches.',
			ensureTermination:
				'Ensure that all paths in your script are able to terminate, i.e. no infinite loops.',
			increaseTimeout: `If your task can reasonably take more than ${taskTimeout} ${taskTimeout === 1 ? 'second' : 'seconds'}, increase the timeout using the N8N_RUNNERS_TASK_TIMEOUT environment variable.`,
		};

		const suggestions = [fixes.optimizeScript, fixes.ensureTermination];

		if (isSelfHosted) suggestions.push(fixes.increaseTimeout);

		const suggestionsText = suggestions
			.map((suggestion, index) => `${index + 1}. ${suggestion}`)
			.join('<br/>');

		const description = `${mode === 'internal' ? subtitles.internal : subtitles.external} You can try the following:<br/><br/>${suggestionsText}`;

		this.description = description;
	}
}
