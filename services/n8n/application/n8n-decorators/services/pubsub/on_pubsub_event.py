"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/pubsub/on-pubsub-event.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/pubsub 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./pubsub-metadata、../errors、../types。导出:OnPubSubEvent。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/pubsub/on-pubsub-event.ts -> services/n8n/application/n8n-decorators/services/pubsub/on_pubsub_event.py

import { Container } from '@n8n/di';

import { PubSubMetadata } from './pubsub-metadata';
import type { PubSubEventName, PubSubEventFilter } from './pubsub-metadata';
import { NonMethodError } from '../errors';
import type { EventHandlerClass } from '../types';

/**
 * Decorator that registers a method to be called when a specific PubSub event occurs.
 * Optionally filters event handling based on instance type and role.
 *
 * @param eventName - The PubSub event to listen for
 * @param filter - Optional filter to limit event handling to specific instance types or roles
 *
 * @example
 *
 * ```ts
 * @Service()
 * class MyService {
 *   @OnPubSubEvent('community-package-install', { instanceType: 'main', instanceRole: 'leader' })
 *   async handlePackageInstall() {
 *     // Handle community package installation
 *   }
 * }
 * ```
 */
export const OnPubSubEvent =
	(eventName: PubSubEventName, filter?: PubSubEventFilter): MethodDecorator =>
	(prototype, propertyKey, descriptor) => {
		const eventHandlerClass = prototype.constructor as EventHandlerClass;
		const methodName = String(propertyKey);

		if (typeof descriptor?.value !== 'function') {
			throw new NonMethodError(`${eventHandlerClass.name}.${methodName}()`);
		}

		Container.get(PubSubMetadata).register({
			eventHandlerClass,
			methodName,
			eventName,
			filter,
		});
	};
