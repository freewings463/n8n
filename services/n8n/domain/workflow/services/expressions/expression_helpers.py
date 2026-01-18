"""
MIGRATION-META:
  source_path: packages/workflow/src/expressions/expression-helpers.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/expressions 的工作流工具。导入/依赖:外部:无；内部:无；本地:无。导出:isExpression。关键函数/方法:isExpression。用于提供工作流通用工具能力（纯函数/封装器）供复用。注释目标:Checks if the given value is an expression. An expression is a string that / starts with '='.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/expressions/expression-helpers.ts -> services/n8n/domain/workflow/services/expressions/expression_helpers.py

/**
 * Checks if the given value is an expression. An expression is a string that
 * starts with '='.
 */
export const isExpression = (expr: unknown): expr is string => {
	if (typeof expr !== 'string') return false;

	return expr.charAt(0) === '=';
};
