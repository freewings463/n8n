"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/assert.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/utils/src 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:assert。关键函数/方法:assert。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Asserts given condition。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Generic shared utilities -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/assert.ts -> services/n8n/application/n8n-utils/services/utils/assert.py

/**
 * Asserts given condition
 */
export function assert(condition: unknown, message?: string): asserts condition {
	if (!condition) {
		// eslint-disable-next-line n8n-local-rules/no-plain-errors
		throw new Error(message ?? 'Assertion failed');
	}
}
