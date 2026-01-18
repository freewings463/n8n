"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/memoized.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的模块。导入/依赖:外部:node:assert；内部:无；本地:无。导出:Memoized。关键函数/方法:assert。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/memoized.ts -> services/n8n/infrastructure/n8n-decorators/container/src/memoized.py

import assert from 'node:assert';

/**
 * A decorator that implements memoization for class property getters.
 *
 * The decorated getter will only be executed once and its value cached for subsequent access
 *
 * @example
 * class Example {
 *   @Memoized
 *   get computedValue() {
 *     // This will only run once and the result will be cached
 *     return heavyComputation();
 *   }
 * }
 *
 * @throws If decorator is used on something other than a getter
 */
export function Memoized<T = unknown>(
	target: object,
	propertyKey: string | symbol,
	descriptor?: TypedPropertyDescriptor<T>,
): TypedPropertyDescriptor<T> {
	const originalGetter = descriptor?.get;
	assert(originalGetter, '@Memoized can only be used on getters');

	// Replace the original getter for the first call
	descriptor.get = function (this: typeof target.constructor): T {
		const value = originalGetter.call(this);
		// Add a property on the class instance to stop reading from the getter on class prototype
		Object.defineProperty(this, propertyKey, {
			value,
			configurable: false,
			enumerable: false,
			writable: false,
		});
		return value;
	};

	return descriptor;
}
