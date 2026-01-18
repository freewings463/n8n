"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/debounce.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的模块。导入/依赖:外部:lodash/debounce；内部:无；本地:无。导出:Debounce。关键函数/方法:get。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/debounce.ts -> services/n8n/infrastructure/n8n-decorators/container/src/debounce.py

import debounce from 'lodash/debounce';

/**
 * Debounce a class method using `lodash/debounce`.
 *
 * @param waitMs - Number of milliseconds to debounce method by.
 *
 * @example
 * ```
 * class MyClass {
 *   @Debounce(1000)
 *   async myMethod() {
 *     // debounced
 *   }
 * }
 * ```
 */
export const Debounce =
	(waitMs: number): MethodDecorator =>
	<T>(
		_: object,
		methodName: string | symbol,
		originalDescriptor: PropertyDescriptor,
	): TypedPropertyDescriptor<T> => ({
		configurable: true,

		get() {
			const debouncedFn = debounce(originalDescriptor.value, waitMs);

			Object.defineProperty(this, methodName, {
				configurable: false,
				value: debouncedFn,
			});

			return debouncedFn as T;
		},
	});
