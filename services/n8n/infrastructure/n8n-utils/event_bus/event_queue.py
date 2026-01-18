"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/event-queue.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/utils/src 的队列工具。导入/依赖:外部:无；内部:无；本地:无。导出:createEventQueue。关键函数/方法:processNext、enqueue。用于提供队列通用工具能力（纯函数/封装器）供复用。注释目标:Create an event queue that processes events sequentially.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Event bus/queue helpers -> infrastructure/event_bus
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/event-queue.ts -> services/n8n/infrastructure/n8n-utils/event_bus/event_queue.py

/**
 * Create an event queue that processes events sequentially.
 *
 * @param processEvent - Async function that processes a single event.
 * @returns A function that enqueues events for processing.
 */
export function createEventQueue<T>(processEvent: (event: T) => Promise<void>) {
	// The internal queue holding events.
	const queue: T[] = [];

	// Flag to indicate whether an event is currently being processed.
	let processing = false;

	/**
	 * Process the next event in the queue (if not already processing).
	 */
	async function processNext(): Promise<void> {
		if (processing || queue.length === 0) {
			return;
		}

		processing = true;
		const currentEvent = queue.shift();

		if (currentEvent !== undefined) {
			try {
				await processEvent(currentEvent);
			} catch (error) {
				console.error('Error processing event:', error);
			}
		}

		processing = false;

		// Recursively process the next event.
		await processNext();
	}

	/**
	 * Enqueue an event and trigger processing.
	 *
	 * @param event - The event to enqueue.
	 */
	function enqueue(event: T): void {
		queue.push(event);
		void processNext();
	}

	return { enqueue };
}
