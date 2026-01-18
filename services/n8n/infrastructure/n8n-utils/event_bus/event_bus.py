"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/event-bus.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/utils/src 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:CallbackFn、EventBus、createEventBus。关键函数/方法:on、once、fn、off、emit、handler。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Event bus/queue helpers -> infrastructure/event_bus
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/event-bus.ts -> services/n8n/infrastructure/n8n-utils/event_bus/event_bus.py

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type CallbackFn = (...args: any[]) => any;

type Payloads<ListenerMap> = {
	[E in keyof ListenerMap]: unknown;
};

type Listener<Payload> = (payload: Payload) => void;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export interface EventBus<ListenerMap extends Payloads<ListenerMap> = Record<string, any>> {
	on<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		fn: Listener<ListenerMap[EventName]>,
	): void;

	once<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		fn: Listener<ListenerMap[EventName]>,
	): void;

	off<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		fn: Listener<ListenerMap[EventName]>,
	): void;

	emit<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		event?: ListenerMap[EventName],
	): void;
}

/**
 * Creates an event bus with the given listener map.
 *
 * @example
 * ```ts
 * const eventBus = createEventBus<{
 *   'user-logged-in': { username: string };
 *   'user-logged-out': never;
 * }>();
 */
export function createEventBus<
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	ListenerMap extends Payloads<ListenerMap> = Record<string, any>,
>(): EventBus<ListenerMap> {
	const handlers = new Map<string, CallbackFn[]>();

	return {
		on(eventName, fn) {
			let eventFns = handlers.get(eventName);
			if (!eventFns) {
				eventFns = [fn];
			} else {
				eventFns.push(fn);
			}
			handlers.set(eventName, eventFns);
		},

		once(eventName, fn) {
			const handler: typeof fn = (payload) => {
				this.off(eventName, handler);
				fn(payload);
			};
			this.on(eventName, handler);
		},

		off(eventName, fn) {
			const eventFns = handlers.get(eventName);
			if (eventFns) {
				eventFns.splice(eventFns.indexOf(fn) >>> 0, 1);
			}
		},

		emit(eventName, event) {
			const eventFns = handlers.get(eventName);
			if (eventFns) {
				eventFns.slice().forEach((handler) => {
					handler(event);
				});
			}
		},
	};
}
