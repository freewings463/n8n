"""
MIGRATION-META:
  source_path: packages/workflow/src/evaluation-helpers.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流工具。导入/依赖:外部:无；内部:无；本地:无。导出:DEFAULT_EVALUATION_METRIC、metricRequiresModelConnection。关键函数/方法:metricRequiresModelConnection。用于提供工作流通用工具能力（纯函数/封装器）供复用。注释目标:Evaluation-related utility functions / This file contains utilities that need to be shared between different packages。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/evaluation-helpers.ts -> services/n8n/domain/workflow/services/evaluation_helpers.py

/**
 * Evaluation-related utility functions
 *
 * This file contains utilities that need to be shared between different packages
 * to avoid circular dependencies. For example, the evaluation test-runner (in CLI package)
 * and the Evaluation node (in nodes-base package) both need to know which metrics
 * require AI model connections, but they can't import from each other directly.
 *
 * By placing shared utilities here in the workflow package (which both packages depend on),
 * we avoid circular dependency issues.
 */

/**
 * Default metric type used in evaluations
 */
export const DEFAULT_EVALUATION_METRIC = 'correctness';

/**
 * Determines if a given evaluation metric requires an AI model connection
 * @param metric The metric name to check
 * @returns true if the metric requires an AI model connection
 */
export function metricRequiresModelConnection(metric: string): boolean {
	return ['correctness', 'helpfulness'].includes(metric);
}
