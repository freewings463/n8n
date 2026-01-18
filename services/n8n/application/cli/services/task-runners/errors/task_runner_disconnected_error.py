"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/task-runner-disconnected-error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:@n8n/task-runner、n8n-workflow；本地:无。导出:TaskRunnerDisconnectedError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/task-runner-disconnected-error.ts -> services/n8n/application/cli/services/task-runners/errors/task_runner_disconnected_error.py

import type { TaskRunner } from '@n8n/task-runner';
import { UnexpectedError } from 'n8n-workflow';

export class TaskRunnerDisconnectedError extends UnexpectedError {
	description: string;

	constructor(
		readonly runnerId: TaskRunner['id'],
		isCloudDeployment: boolean,
	) {
		super('Node execution failed');

		const fixSuggestions = {
			reduceItems:
				'Reduce the number of items processed at a time, by batching them using a loop node',
			increaseMemory:
				"Increase the memory available to the task runner with 'N8N_RUNNERS_MAX_OLD_SPACE_SIZE' environment variable",
			upgradePlan: 'Upgrade your cloud plan to increase the available memory',
		};

		const subtitle =
			'This can happen for various reasons. Please try executing the node again. If the problem persists, you can try the following:';
		const suggestions = isCloudDeployment
			? [fixSuggestions.reduceItems, fixSuggestions.upgradePlan]
			: [fixSuggestions.reduceItems, fixSuggestions.increaseMemory];
		const suggestionsText = suggestions
			.map((suggestion, index) => `${index + 1}. ${suggestion}`)
			.join('<br/>');

		const description = `${subtitle}<br/><br/>${suggestionsText}`;

		this.description = description;
	}
}
