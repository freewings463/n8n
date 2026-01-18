"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/timed.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:TimedOptions、Timed。关键函数/方法:warn。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/timed.ts -> services/n8n/infrastructure/n8n-decorators/container/src/timed.py

export interface TimedOptions {
	/** Duration (in ms) above which to log a warning. Defaults to `100`. */
	threshold?: number;
	/** Whether to include method parameters in the log. Defaults to `false`. */
	logArgs?: boolean;
}

interface Logger {
	warn(message: string, meta?: object): void;
}

/**
 * Factory to create decorators to warn when method calls exceed a duration threshold.
 */
export const Timed =
	(logger: Logger, msg = 'Slow method call') =>
	(options: TimedOptions = {}): MethodDecorator =>
	(_target, propertyKey, descriptor: PropertyDescriptor) => {
		const originalMethod = descriptor.value as (...args: unknown[]) => unknown;
		const thresholdMs = options.threshold ?? 100;
		const logArgs = options.logArgs ?? false;

		descriptor.value = async function (...args: unknown[]) {
			const methodName = `${this.constructor.name}.${String(propertyKey)}`;
			const start = performance.now();
			const result = await originalMethod.apply(this, args);
			const durationMs = performance.now() - start;

			if (durationMs > thresholdMs) {
				logger.warn(msg, {
					method: methodName,
					durationMs: Math.round(durationMs),
					thresholdMs,
					params: logArgs ? args : '[hidden]',
				});
			}

			return result;
		};

		return descriptor;
	};
