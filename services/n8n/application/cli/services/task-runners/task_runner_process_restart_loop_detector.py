"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-runner-process-restart-loop-detector.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners 的模块。导入/依赖:外部:无；内部:@n8n/constants、@/task-runners/…/task-runner-restart-loop-error、@/typed-emitter；本地:./task-runner-process-base。导出:TaskRunnerProcessRestartLoopDetector。关键函数/方法:increment、reset、isMaxCountExceeded、msSinceFirstIncrement。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-runner-process-restart-loop-detector.ts -> services/n8n/application/cli/services/task-runners/task_runner_process_restart_loop_detector.py

import { Time } from '@n8n/constants';

import { TaskRunnerRestartLoopError } from '@/task-runners/errors/task-runner-restart-loop-error';
import { TypedEmitter } from '@/typed-emitter';

import type { TaskRunnerProcessBase } from './task-runner-process-base';

const MAX_RESTARTS = 5;
const RESTARTS_WINDOW = 2 * Time.seconds.toMilliseconds;

type TaskRunnerProcessRestartLoopDetectorEventMap = {
	'restart-loop-detected': TaskRunnerRestartLoopError;
};

/**
 * A class to monitor the task runner process for restart loops
 */
export class TaskRunnerProcessRestartLoopDetector extends TypedEmitter<TaskRunnerProcessRestartLoopDetectorEventMap> {
	/**
	 * How many times the process needs to restart for it to be detected
	 * being in a loop.
	 */
	private readonly maxCount = MAX_RESTARTS;

	/**
	 * The time interval in which the process needs to restart `maxCount` times
	 * to be detected as being in a loop.
	 */
	private readonly restartsWindow = RESTARTS_WINDOW;

	private numRestarts = 0;

	/** Time when the first restart of a loop happened within a time window */
	private firstRestartedAt = Date.now();

	constructor(private readonly taskRunnerProcess: TaskRunnerProcessBase) {
		super();

		this.taskRunnerProcess.on('exit', () => {
			this.increment();

			if (this.isMaxCountExceeded()) {
				this.emit(
					'restart-loop-detected',
					new TaskRunnerRestartLoopError(this.numRestarts, this.msSinceFirstIncrement()),
				);
			}
		});
	}

	/**
	 * Increments the counter
	 */
	private increment() {
		const now = Date.now();
		if (now > this.firstRestartedAt + this.restartsWindow) {
			this.reset();
		}

		this.numRestarts++;
	}

	private reset() {
		this.numRestarts = 0;
		this.firstRestartedAt = Date.now();
	}

	private isMaxCountExceeded() {
		return this.numRestarts >= this.maxCount;
	}

	private msSinceFirstIncrement() {
		return Date.now() - this.firstRestartedAt;
	}
}
