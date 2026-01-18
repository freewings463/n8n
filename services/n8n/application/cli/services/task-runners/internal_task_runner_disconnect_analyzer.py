"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/internal-task-runner-disconnect-analyzer.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@/task-runners/…/task-broker-types；本地:./default-task-runner-disconnect-analyzer、./errors/task-runner-oom-error、./sliding-window-signal、./task-runner-process-base 等1项。导出:InternalTaskRunnerDisconnectAnalyzer。关键函数/方法:toDisconnectError、awaitExitSignal。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/internal-task-runner-disconnect-analyzer.ts -> services/n8n/application/cli/services/task-runners/internal_task_runner_disconnect_analyzer.py

import { TaskRunnersConfig } from '@n8n/config';
import { Service } from '@n8n/di';

import type { DisconnectErrorOptions } from '@/task-runners/task-broker/task-broker-types';

import { DefaultTaskRunnerDisconnectAnalyzer } from './default-task-runner-disconnect-analyzer';
import { TaskRunnerOomError } from './errors/task-runner-oom-error';
import { SlidingWindowSignal } from './sliding-window-signal';
import type { ExitReason, TaskRunnerProcessEventMap } from './task-runner-process-base';
import { JsTaskRunnerProcess } from './task-runner-process-js';

/**
 * Analyzes the disconnect reason of a task runner process to provide a more
 * meaningful error message to the user.
 */
@Service()
export class InternalTaskRunnerDisconnectAnalyzer extends DefaultTaskRunnerDisconnectAnalyzer {
	private readonly exitReasonSignal: SlidingWindowSignal<TaskRunnerProcessEventMap, 'exit'>;

	constructor(
		private readonly runnerConfig: TaskRunnersConfig,
		private readonly taskRunnerProcess: JsTaskRunnerProcess,
	) {
		super();

		// When the task runner process is running as a child process, there's
		// no determinate time when it exits compared to when the runner disconnects
		// (i.e. it's a race condition). Hence we use a sliding window to determine
		// the exit reason. As long as we receive the exit signal from the task
		// runner process within the window, we can determine the exit reason.
		this.exitReasonSignal = new SlidingWindowSignal(this.taskRunnerProcess, 'exit', {
			windowSizeInMs: 500,
		});
	}

	async toDisconnectError(opts: DisconnectErrorOptions): Promise<Error> {
		const exitCode = await this.awaitExitSignal();
		if (exitCode === 'oom') {
			return new TaskRunnerOomError(opts.runnerId ?? 'Unknown runner ID', this.isCloudDeployment);
		}

		return await super.toDisconnectError(opts);
	}

	private async awaitExitSignal(): Promise<ExitReason> {
		if (this.runnerConfig.mode === 'external') {
			// If the task runner is running in external mode, we don't have
			// control over the process and hence cannot determine the exit
			// reason. We just return 'unknown' in this case.
			return 'unknown';
		}

		const lastExitReason = await this.exitReasonSignal.getSignal();

		return lastExitReason?.reason ?? 'unknown';
	}
}
