"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/task-runner-oom-error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow、@/task-runners/…/task-broker.service；本地:无。导出:TaskRunnerOomError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/task-runner-oom-error.ts -> services/n8n/application/cli/services/task-runners/errors/task_runner_oom_error.py

import { UserError } from 'n8n-workflow';

import type { TaskRunner } from '@/task-runners/task-broker/task-broker.service';

export class TaskRunnerOomError extends UserError {
	description: string;

	constructor(
		readonly runnerId: TaskRunner['id'],
		isCloudDeployment: boolean,
	) {
		super('Node ran out of memory');

		const fixSuggestions = {
			reduceItems:
				'Reduce the number of items processed at a time, by batching them using a loop node',
			increaseMemory:
				"Increase the memory available to the task runner with 'N8N_RUNNERS_MAX_OLD_SPACE_SIZE' environment variable",
			upgradePlan: 'Upgrade your cloud plan to increase the available memory',
		};

		const subtitle =
			'This usually happens when there are too many items to process. You can try the following:';
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
