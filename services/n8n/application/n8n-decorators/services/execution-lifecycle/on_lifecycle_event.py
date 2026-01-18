"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/execution-lifecycle/on-lifecycle-event.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/execution-lifecycle 的执行模块。导入/依赖:外部:无；内部:@n8n/di；本地:./lifecycle-metadata、../errors。导出:OnLifecycleEvent。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/execution-lifecycle/on-lifecycle-event.ts -> services/n8n/application/n8n-decorators/services/execution-lifecycle/on_lifecycle_event.py

import { Container } from '@n8n/di';

import type { LifecycleEvent, LifecycleHandlerClass } from './lifecycle-metadata';
import { LifecycleMetadata } from './lifecycle-metadata';
import { NonMethodError } from '../errors';

/**
 * Decorator that registers a method to be called when a specific lifecycle event occurs.
 * For more information, see `execution-lifecycle-hooks.ts` in `cli` and `core`.
 *
 * @example
 *
 * ```ts
 * @Service()
 * class MyService {
 *   @OnLifecycleEvent('workflowExecuteAfter')
 *   async handleEvent(ctx: WorkflowExecuteAfterContext) {
 *     // ...
 *   }
 * }
 * ```
 */
export const OnLifecycleEvent =
	(eventName: LifecycleEvent): MethodDecorator =>
	(prototype, propertyKey, descriptor) => {
		const handlerClass = prototype.constructor as LifecycleHandlerClass;
		const methodName = String(propertyKey);

		if (typeof descriptor?.value !== 'function') {
			throw new NonMethodError(`${handlerClass.name}.${methodName}()`);
		}

		Container.get(LifecycleMetadata).register({
			handlerClass,
			methodName,
			eventName,
		});
	};
