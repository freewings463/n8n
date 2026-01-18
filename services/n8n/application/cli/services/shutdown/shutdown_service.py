"""
MIGRATION-META:
  source_path: packages/cli/src/shutdown/shutdown.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/shutdown 的服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/decorators、@n8n/di、n8n-core、n8n-workflow；本地:无。导出:ComponentShutdownError、ShutdownService。关键函数/方法:register、validate、shutdown、waitForShutdown、isShuttingDown、startShutdown、shutdownComponent、assert。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/shutdown/shutdown.service.ts -> services/n8n/application/cli/services/shutdown/shutdown_service.py

import { Logger } from '@n8n/backend-common';
import type { ShutdownHandler } from '@n8n/decorators';
import { ShutdownMetadata } from '@n8n/decorators';
import { Container, Service } from '@n8n/di';
import { ErrorReporter } from 'n8n-core';
import { assert, UnexpectedError, UserError } from 'n8n-workflow';

/** Error reported when a listener fails to shutdown gracefully */
export class ComponentShutdownError extends UnexpectedError {
	constructor(componentName: string, cause: Error) {
		super('Failed to shutdown gracefully', {
			cause,
			extra: { component: componentName },
		});
	}
}

/** Service responsible for orchestrating a graceful shutdown of the application */
@Service()
export class ShutdownService {
	private shutdownPromise: Promise<void> | undefined;

	constructor(
		private readonly logger: Logger,
		private readonly errorReporter: ErrorReporter,
		private readonly shutdownMetadata: ShutdownMetadata,
	) {}

	/** Registers given listener to be notified when the application is shutting down */
	register(priority: number, handler: ShutdownHandler) {
		this.shutdownMetadata.register(priority, handler);
	}

	/** Validates that all the registered shutdown handlers are properly configured */
	validate() {
		const handlers = this.shutdownMetadata.getHandlersByPriority().flat();

		for (const { serviceClass, methodName } of handlers) {
			if (!Container.has(serviceClass)) {
				throw new UserError(
					`Component "${serviceClass.name}" is not registered with the DI container. Any component using @OnShutdown() must be decorated with @Service()`,
				);
			}

			const service = Container.get(serviceClass);
			if (!service[methodName]) {
				throw new UserError(
					`Component "${serviceClass.name}" does not have a "${methodName}" method`,
				);
			}
		}
	}

	/** Signals all registered listeners that the application is shutting down */
	shutdown() {
		if (this.shutdownPromise) {
			throw new UnexpectedError('App is already shutting down');
		}

		this.shutdownPromise = this.startShutdown();
	}

	/** Returns a promise that resolves when all the registered listeners have shut down */
	async waitForShutdown(): Promise<void> {
		if (!this.shutdownPromise) {
			throw new UnexpectedError('App is not shutting down');
		}

		await this.shutdownPromise;
	}

	isShuttingDown() {
		return !!this.shutdownPromise;
	}

	private async startShutdown() {
		const handlers = Object.values(this.shutdownMetadata.getHandlersByPriority()).reverse();

		for (const handlerGroup of handlers) {
			await Promise.allSettled(
				handlerGroup.map(async (handler) => await this.shutdownComponent(handler)),
			);
		}
	}

	private async shutdownComponent({ serviceClass, methodName }: ShutdownHandler) {
		const name = `${serviceClass.name}.${methodName}()`;
		try {
			this.logger.debug(`Shutting down component "${name}"`);
			const service = Container.get(serviceClass);
			const method = service[methodName];
			await method.call(service);
		} catch (error) {
			assert(error instanceof Error);
			this.errorReporter.error(new ComponentShutdownError(name, error));
		}
	}
}
