"""
MIGRATION-META:
  source_path: packages/cli/src/typed-emitter.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src 的模块。导入/依赖:外部:lodash/debounce；内部:无；本地:无。导出:TypedEmitter。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/typed-emitter.ts -> services/n8n/application/cli/services/typed_emitter.py

import debounce from 'lodash/debounce';
import { EventEmitter } from 'node:events';

type Payloads<ListenerMap> = {
	[E in keyof ListenerMap]: unknown;
};

type Listener<Payload> = (payload: Payload) => void;

export class TypedEmitter<ListenerMap extends Payloads<ListenerMap>> extends EventEmitter {
	private debounceWait = 300; // milliseconds

	override on<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		listener: Listener<ListenerMap[EventName]>,
	) {
		return super.on(eventName, listener);
	}

	override once<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		listener: Listener<ListenerMap[EventName]>,
	) {
		return super.once(eventName, listener);
	}

	override off<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		listener: Listener<ListenerMap[EventName]>,
	) {
		return super.off(eventName, listener);
	}

	override emit<EventName extends keyof ListenerMap & string>(
		eventName: EventName,
		payload?: ListenerMap[EventName],
	): boolean {
		return super.emit(eventName, payload);
	}

	protected debouncedEmit = debounce(
		<EventName extends keyof ListenerMap & string>(
			eventName: EventName,
			payload?: ListenerMap[EventName],
		) => super.emit(eventName, payload),
		this.debounceWait,
	);
}
