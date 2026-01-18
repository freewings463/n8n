"""
MIGRATION-META:
  source_path: packages/core/src/utils/deep-merge.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:deepMerge。关键函数/方法:isPlainObject。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Checks if a value is a plain object (not an array, null, or other type).。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core utility helpers -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/utils/deep-merge.ts -> services/n8n/application/core/services/utils/deep_merge.py

/**
 * Checks if a value is a plain object (not an array, null, or other type).
 */
function isPlainObject(value: unknown): value is Record<string, unknown> {
	return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/**
 * This function performs a deep merge of two objects.
 * Source properties override target properties. Nested objects are merged recursively.
 * Arrays and non-object values from source replace those in target.
 *
 * @param target The target object to merge into.
 * @param source The source object to merge from.
 * @returns A new object that is the result of merging source into target.
 */
export function deepMerge<T>(target: T, source: Partial<T>): T {
	// Handle null/undefined source - return a shallow copy of target
	if (source === null || source === undefined) {
		return isPlainObject(target) ? { ...target } : target;
	}

	// Handle null/undefined target - return a shallow copy of source
	if (target === null || target === undefined) {
		return source as T;
	}

	// If either value is not a plain object, source wins
	if (!isPlainObject(target) || !isPlainObject(source)) {
		return source as T;
	}

	// Both are plain objects - perform deep merge
	const result = { ...target } as Record<string, unknown>;
	const sourceRecord = source as Record<string, unknown>;

	for (const key of Object.keys(sourceRecord)) {
		// Prevent prototype pollution
		if (['__proto__', 'constructor', 'prototype'].includes(key)) continue;

		const sourceValue = sourceRecord[key];
		const targetValue = result[key];

		if (isPlainObject(sourceValue) && isPlainObject(targetValue)) {
			// Both values are objects - recurse
			result[key] = deepMerge(targetValue, sourceValue);
		} else {
			// Source value replaces target value
			result[key] = sourceValue;
		}
	}

	return result as T;
}
