"""
MIGRATION-META:
  source_path: packages/cli/src/utils/sliding-window.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:SlidingWindowOptions、SlidingWindow。关键函数/方法:addEvent、getCount、clear。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Configuration options for the SlidingWindow。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utils/sliding-window.ts -> services/n8n/application/cli/services/utils/sliding_window.py

/**
 * Configuration options for the SlidingWindow
 */
export interface SlidingWindowOptions {
	/** Maximum number of events to track for rate limiting purposes */
	maxEvents: number;
	/** Duration of the sliding window in milliseconds */
	durationMs: number;
}

/**
 * A sliding window implementation for tracking events within a time window.
 * Useful for rate limiting, monitoring event frequencies, or implementing circuit breakers.
 *
 * @example
 * ```typescript
 * const window = new SlidingWindow({ maxEvents: 100, durationMs: 60000 }); // 100 events per minute
 * window.addEvent(Date.now());
 * const count = window.getCount(); // Returns number of events in the last minute
 * ```
 */
export class SlidingWindow {
	private maxEvents: number;
	private durationMs: number;
	private eventTimestamps: number[] = [];

	/**
	 * Creates a new SlidingWindow instance
	 * @param options - Configuration for the sliding window
	 */
	constructor(options: SlidingWindowOptions) {
		this.maxEvents = options.maxEvents;
		this.durationMs = options.durationMs;
	}

	/**
	 * Adds an event timestamp to the sliding window.
	 * Automatically prunes the internal array if it grows beyond 2x maxEvents to prevent unbounded growth.
	 *
	 * @param timestamp - Unix timestamp in milliseconds of when the event occurred
	 */
	addEvent(timestamp: number) {
		this.eventTimestamps.push(timestamp);

		// Remove events if they exceed the maximum allowed maxEvents times 2
		if (this.eventTimestamps.length > this.maxEvents * 2) {
			this.eventTimestamps = this.eventTimestamps.slice(-this.maxEvents * 2);
		}
	}

	/**
	 * Gets the count of events within the current sliding window.
	 * Removes expired events that fall outside the time window before returning the count.
	 *
	 * @returns The number of events that occurred within the sliding window duration from now
	 */
	getCount() {
		const now = Date.now();
		const windowStart = now - this.durationMs;
		this.eventTimestamps = this.eventTimestamps.filter((timestamp) => timestamp >= windowStart);
		return this.eventTimestamps.length;
	}

	/**
	 * Clears all tracked events from the sliding window
	 */
	clear() {
		this.eventTimestamps = [];
	}
}
