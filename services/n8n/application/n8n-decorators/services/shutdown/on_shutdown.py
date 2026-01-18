"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/shutdown/on-shutdown.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/shutdown 的模块。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:./constants、./shutdown-metadata、./types。导出:OnShutdown。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/shutdown/on-shutdown.ts -> services/n8n/application/n8n-decorators/services/shutdown/on_shutdown.py

import { Container } from '@n8n/di';
import { UnexpectedError } from 'n8n-workflow';

import { DEFAULT_SHUTDOWN_PRIORITY } from './constants';
import { ShutdownMetadata } from './shutdown-metadata';
import type { ShutdownServiceClass } from './types';

/**
 * Decorator that registers a method as a shutdown hook. The method will
 * be called when the application is shutting down.
 *
 * Priority is used to determine the order in which the hooks are called.
 *
 * NOTE: Requires also @Service() decorator to be used on the class.
 *
 * @example
 * ```ts
 * @Service()
 * class MyClass {
 *   @OnShutdown()
 *   async shutdown() {
 * 	   // Will be called when the app is shutting down
 *   }
 * }
 * ```
 */
export const OnShutdown =
	(priority = DEFAULT_SHUTDOWN_PRIORITY): MethodDecorator =>
	(prototype, propertyKey, descriptor) => {
		const serviceClass = prototype.constructor as ShutdownServiceClass;
		const methodName = String(propertyKey);
		// TODO: assert that serviceClass is decorated with @Service
		if (typeof descriptor?.value === 'function') {
			Container.get(ShutdownMetadata).register(priority, { serviceClass, methodName });
		} else {
			const name = `${serviceClass.name}.${methodName}()`;
			throw new UnexpectedError(
				`${name} must be a method on ${serviceClass.name} to use "OnShutdown"`,
			);
		}
	};
