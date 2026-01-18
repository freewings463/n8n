"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/multi-main/on-multi-main-event.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/multi-main 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./multi-main-metadata、../errors、../types。导出:OnLeaderTakeover、OnLeaderStepdown。关键函数/方法:OnLeaderTakeover、OnLeaderStepdown。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/multi-main/on-multi-main-event.ts -> services/n8n/application/n8n-decorators/services/multi-main/on_multi_main_event.py

import { Container } from '@n8n/di';

import type { MultiMainEvent } from './multi-main-metadata';
import {
	LEADER_TAKEOVER_EVENT_NAME,
	LEADER_STEPDOWN_EVENT_NAME,
	MultiMainMetadata,
} from './multi-main-metadata';
import { NonMethodError } from '../errors';
import type { EventHandlerClass } from '../types';

const OnMultiMainEvent =
	(eventName: MultiMainEvent): MethodDecorator =>
	(prototype, propertyKey, descriptor) => {
		const eventHandlerClass = prototype.constructor as EventHandlerClass;
		const methodName = String(propertyKey);

		if (typeof descriptor?.value !== 'function') {
			throw new NonMethodError(`${eventHandlerClass.name}.${methodName}()`);
		}

		Container.get(MultiMainMetadata).register({
			eventHandlerClass,
			methodName,
			eventName,
		});
	};

/**
 * Decorator that registers a method to be called when this main instance becomes the leader.
 *
 * @example
 *
 * ```ts
 * @Service()
 * class MyService {
 *   @OnLeaderTakeover()
 *   async startDoingThings() {
 *     // ...
 *   }
 * }
 * ```
 */
export const OnLeaderTakeover = () => OnMultiMainEvent(LEADER_TAKEOVER_EVENT_NAME);

/**
 * Decorator that registers a method to be called when this main instance stops being the leader.
 *
 * @example
 *
 * ```ts
 * @Service()
 * class MyService {
 *   @OnLeaderStepdown()
 *   async stopDoingThings() {
 *     // ...
 *   }
 * }
 * ```
 */
export const OnLeaderStepdown = () => OnMultiMainEvent(LEADER_STEPDOWN_EVENT_NAME);
