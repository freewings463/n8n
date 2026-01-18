"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/sliding-window-signal.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners 的模块。导入/依赖:外部:无；内部:无；本地:../typed-emitter。导出:SlidingWindowSignalOpts、SlidingWindowSignal。关键函数/方法:getSignal、onExit、resolve。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/sliding-window-signal.ts -> services/n8n/application/cli/services/task-runners/sliding_window_signal.py

import type { TypedEmitter } from '../typed-emitter';

export type SlidingWindowSignalOpts = {
	windowSizeInMs?: number;
};

/**
 * A class that listens for a specific event on an emitter (signal) and
 * provides a sliding window of the last event that was emitted.
 */
export class SlidingWindowSignal<TEvents, TEventName extends keyof TEvents & string> {
	private lastSignal: TEvents[TEventName] | null = null;

	private lastSignalTime: number = 0;

	private windowSizeInMs: number;

	constructor(
		private readonly eventEmitter: TypedEmitter<TEvents>,
		private readonly eventName: TEventName,
		opts: SlidingWindowSignalOpts = {},
	) {
		const { windowSizeInMs = 500 } = opts;

		this.windowSizeInMs = windowSizeInMs;

		eventEmitter.on(eventName, (signal: TEvents[TEventName]) => {
			this.lastSignal = signal;
			this.lastSignalTime = Date.now();
		});
	}

	/**
	 * If an event has been emitted within the last `windowSize` milliseconds,
	 * that event is returned. Otherwise it will wait for up to `windowSize`
	 * milliseconds for the event to be emitted. `null` is returned
	 * if no event is emitted within the window.
	 */
	async getSignal(): Promise<TEvents[TEventName] | null> {
		const timeSinceLastEvent = Date.now() - this.lastSignalTime;
		if (timeSinceLastEvent <= this.windowSizeInMs) return this.lastSignal;

		return await new Promise<TEvents[TEventName] | null>((resolve) => {
			let timeoutTimerId: NodeJS.Timeout | null = null;

			const onExit = (signal: TEvents[TEventName]) => {
				if (timeoutTimerId) clearTimeout(timeoutTimerId);
				resolve(signal);
			};

			timeoutTimerId = setTimeout(() => {
				this.eventEmitter.off(this.eventName, onExit);
				resolve(null);
			});

			this.eventEmitter.once(this.eventName, onExit);
		});
	}
}
