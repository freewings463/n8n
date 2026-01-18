"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/errors/timeout-error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner/errors 的错误。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:TimeoutError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/errors/timeout-error.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/errors/timeout_error.py

import { ApplicationError } from '@n8n/errors';

export class TimeoutError extends ApplicationError {
	description: string;

	constructor(taskTimeout: number) {
		super(
			`Task execution timed out after ${taskTimeout} ${taskTimeout === 1 ? 'second' : 'seconds'}`,
		);

		const subtitle = 'The task runner was taking too long on this task, so the task was aborted.';

		const fixes = {
			optimizeScript:
				'Optimize your script to prevent long-running tasks, e.g. by processing data in smaller batches.',
			ensureTermination:
				'Ensure that all paths in your script are able to terminate, i.e. no infinite loops.',
		};

		const suggestions = [fixes.optimizeScript, fixes.ensureTermination];

		const suggestionsText = suggestions
			.map((suggestion, index) => `${index + 1}. ${suggestion}`)
			.join('<br/>');

		const description = `${subtitle} You can try the following:<br/><br/>${suggestionsText}`;

		this.description = description;
	}
}
