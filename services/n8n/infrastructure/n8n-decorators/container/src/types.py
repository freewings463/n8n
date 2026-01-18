"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Class、EventHandlerClass、EventHandler。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/types.ts -> services/n8n/infrastructure/n8n-decorators/container/src/types.py

export type Class<T = object, A extends unknown[] = unknown[]> = new (...args: A) => T;

type EventHandlerFn = () => Promise<void> | void;
export type EventHandlerClass = Class<Record<string, EventHandlerFn>>;
export type EventHandler<T extends string> = {
	/** Class holding the method to call on an event. */
	eventHandlerClass: EventHandlerClass;

	/** Name of the method to call on an event. */
	methodName: string;

	/** Name of the event to listen to. */
	eventName: T;
};
