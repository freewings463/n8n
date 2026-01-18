"""
MIGRATION-META:
  source_path: packages/workflow/src/node-parameters/node-parameter-value-type-guard.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/node-parameters 的工作流模块。导入/依赖:外部:无；内部:无；本地:../type-guards。导出:isNodeParameterValue、isAssignmentCollectionValue、isNodeParameters、isValidNodeParameterValueType、assertIsValidNodeParameterValueType。关键函数/方法:isNodeParameterValue、isAssignmentCollectionValue、assignments、isNodeParameters、isValidNodeParameterValueType、isResourceLocatorValue 等3项。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/node-parameters/node-parameter-value-type-guard.ts -> services/n8n/domain/workflow/services/node-parameters/node_parameter_value_type_guard.py

import type {
	AssignmentCollectionValue,
	INodeParameters,
	NodeParameterValue,
	NodeParameterValueType,
} from '../interfaces';
import { isResourceLocatorValue, isResourceMapperValue, isFilterValue } from '../type-guards';

/**
 * Type guard for primitive NodeParameterValue types.
 * Checks if a value is string, number, boolean, undefined, or null.
 */
export function isNodeParameterValue(value: unknown): value is NodeParameterValue {
	return (
		typeof value === 'string' ||
		typeof value === 'number' ||
		typeof value === 'boolean' ||
		value === undefined ||
		value === null
	);
}

/**
 * Type guard for AssignmentCollectionValue.
 * Checks if a value has the structure of an assignment collection.
 */
export function isAssignmentCollectionValue(value: unknown): value is AssignmentCollectionValue {
	if (typeof value !== 'object' || value === null || !('assignments' in value)) {
		return false;
	}

	const assignments = (value as AssignmentCollectionValue).assignments;
	if (!Array.isArray(assignments)) {
		return false;
	}

	return assignments.every(
		(assignment) =>
			typeof assignment === 'object' &&
			assignment !== null &&
			'id' in assignment &&
			'name' in assignment &&
			'value' in assignment &&
			typeof assignment.id === 'string' &&
			typeof assignment.name === 'string' &&
			isNodeParameterValue(assignment.value),
	);
}

/**
 * Type guard for INodeParameters.
 * Recursively validates that all values in the object are valid NodeParameterValueType.
 */
export function isNodeParameters(value: unknown): value is INodeParameters {
	if (typeof value !== 'object' || value === null || Array.isArray(value)) {
		return false;
	}

	// Reject built-in class instances (Date, RegExp, etc.)
	// Only accept plain objects created with {} or Object.create(null)
	if (Object.prototype.toString.call(value) !== '[object Object]') {
		return false;
	}

	// Recursively validate all values
	return Object.values(value).every((val) => isValidNodeParameterValueType(val));
}

/**
 * Comprehensive type guard for NodeParameterValueType.
 * Validates that a value matches any of the valid node parameter value types.
 *
 * @param value - The value to check
 * @returns true if the value is a valid NodeParameterValueType
 *
 * @example
 * ```typescript
 * const value: unknown = { foo: 'bar' };
 * if (isValidNodeParameterValueType(value)) {
 *   // value is now typed as NodeParameterValueType
 * }
 * ```
 */
export function isValidNodeParameterValueType(value: unknown): value is NodeParameterValueType {
	return (
		// Primitives (most common case)
		isNodeParameterValue(value) ||
		// Special object types
		isResourceLocatorValue(value) ||
		isResourceMapperValue(value) ||
		isFilterValue(value) ||
		isAssignmentCollectionValue(value) ||
		// Arrays - all items should be valid NodeParameterValueType
		(Array.isArray(value) &&
			(value.length === 0 ||
				value.every(isNodeParameterValue) ||
				value.every(isNodeParameters) ||
				value.every(isResourceLocatorValue) ||
				value.every(isResourceMapperValue))) ||
		// INodeParameters (must be last to avoid infinite recursion on first check)
		isNodeParameters(value)
	);
}

/**
 * Assertion function that throws if the value is not a valid NodeParameterValueType.
 * Useful for runtime validation with TypeScript type narrowing.
 *
 * @param value - The value to validate
 * @param errorMessage - Optional custom error message
 * @throws Error if the value is not a valid NodeParameterValueType
 *
 * @example
 * ```typescript
 * const value: unknown = getData();
 * assertIsValidNodeParameterValueType(value);
 * // value is now typed as NodeParameterValueType
 * ```
 */
export function assertIsValidNodeParameterValueType(
	value: unknown,
	errorMessage = 'Value is not a valid NodeParameterValueType',
): asserts value is NodeParameterValueType {
	if (!isValidNodeParameterValueType(value)) {
		throw new Error(errorMessage);
	}
}
