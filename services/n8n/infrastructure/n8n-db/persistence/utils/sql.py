"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/sql.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:sql。关键函数/方法:sql。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Provides syntax highlighting for embedded SQL queries in template strings.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/sql.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/sql.py

/**
 * Provides syntax highlighting for embedded SQL queries in template strings.
 */
export function sql(strings: TemplateStringsArray, ...values: string[]): string {
	let result = '';

	// Interleave the strings with the values
	for (let i = 0; i < values.length; i++) {
		result += strings[i];
		result += values[i];
	}

	// Add the last string
	result += strings[strings.length - 1];

	return result;
}
