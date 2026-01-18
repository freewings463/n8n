"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/task-runner-failed-heartbeat.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:TaskRunnerFailedHeartbeatError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/task-runner-failed-heartbeat.error.ts -> services/n8n/application/cli/services/task-runners/errors/task_runner_failed_heartbeat_error.py

import { UserError } from 'n8n-workflow';

export class TaskRunnerFailedHeartbeatError extends UserError {
	description: string;

	constructor(heartbeatInterval: number, isSelfHosted: boolean) {
		super('Task execution aborted because runner became unresponsive');

		const subtitle =
			'The task runner failed to respond as expected, so it was considered unresponsive, and the task was aborted. You can try the following:';

		const fixes = {
			optimizeScript:
				'Optimize your script to prevent CPU-intensive operations, e.g. by breaking them down into smaller chunks or batch processing.',
			ensureTermination:
				'Ensure that all paths in your script are able to terminate, i.e. no infinite loops.',
			increaseInterval: `If your task can reasonably keep the task runner busy for more than ${heartbeatInterval} ${heartbeatInterval === 1 ? 'second' : 'seconds'}, increase the heartbeat interval using the N8N_RUNNERS_HEARTBEAT_INTERVAL environment variable.`,
		};

		const suggestions = [fixes.optimizeScript, fixes.ensureTermination];

		if (isSelfHosted) suggestions.push(fixes.increaseInterval);

		const suggestionsText = suggestions
			.map((suggestion, index) => `${index + 1}. ${suggestion}`)
			.join('<br/>');

		const description = `${subtitle}<br/><br/>${suggestionsText}`;

		this.description = description;
	}
}
