"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/utils/is-object-literal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-common/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:isObjectLiteral。关键函数/方法:isObjectLiteral。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/backend-common treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/utils/is-object-literal.ts -> services/n8n/infrastructure/n8n-backend-common/configuration/utils/is_object_literal.py

type ObjectLiteral = { [key: string | symbol]: unknown };

/**
 * Checks if the provided value is a plain object literal (not null, not an array, not a class instance, and not a primitive).
 * This function serves as a type guard.
 *
 * @param candidate - The value to check
 * @returns {boolean} True if the value is an object literal, false otherwise
 */
export function isObjectLiteral(candidate: unknown): candidate is ObjectLiteral {
	return (
		typeof candidate === 'object' &&
		candidate !== null &&
		!Array.isArray(candidate) &&
		(Object.getPrototypeOf(candidate) as object)?.constructor?.name === 'Object'
	);
}
