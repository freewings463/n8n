"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:EVAL_TYPES、EVAL_USERS、TRACEABLE_NAMES、METRIC_KEYS、DEFAULTS。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:============================================================================ / Evaluation Type Identifiers。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/constants.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/constants.py

// ============================================================================
// Evaluation Type Identifiers
// ============================================================================

export const EVAL_TYPES = {
	PAIRWISE_LOCAL: 'pairwise-local',
	PAIRWISE_LANGSMITH: 'pairwise-langsmith',
	LANGSMITH: 'langsmith-evals',
} as const;

export const EVAL_USERS = {
	PAIRWISE_LOCAL: 'pairwise-local-user',
	LANGSMITH: 'langsmith-eval-user',
} as const;

export const TRACEABLE_NAMES = {
	PAIRWISE_EVALUATION: 'pairwise_evaluation',
	WORKFLOW_GENERATION: 'workflow_generation',
} as const;

// ============================================================================
// LangSmith Metric Keys
// ============================================================================

/**
 * Metric keys for LangSmith evaluation results.
 */
export const METRIC_KEYS = {
	// Single generation metrics
	PAIRWISE_DIAGNOSTIC: 'pairwise_diagnostic',
	PAIRWISE_JUDGES_PASSED: 'pairwise_judges_passed',
	PAIRWISE_PRIMARY: 'pairwise_primary',
	PAIRWISE_TOTAL_PASSES: 'pairwise_total_passes',
	PAIRWISE_TOTAL_VIOLATIONS: 'pairwise_total_violations',

	// Multi-generation metrics
	PAIRWISE_AGGREGATED_DIAGNOSTIC: 'pairwise_aggregated_diagnostic',
	PAIRWISE_GENERATION_CORRECTNESS: 'pairwise_generation_correctness',
	PAIRWISE_GENERATIONS_PASSED: 'pairwise_generations_passed',
	PAIRWISE_TOTAL_JUDGE_CALLS: 'pairwise_total_judge_calls',
} as const;

// ============================================================================
// Default Values
// ============================================================================

export const DEFAULTS = {
	NUM_JUDGES: 3,
	NUM_GENERATIONS: 1,
	EXPERIMENT_NAME: 'pairwise-evals',
	CONCURRENCY: 5,
	REPETITIONS: 1,
	DATASET_NAME: 'notion-pairwise-workflows',
	FEATURE_FLAGS: {
		multiAgent: true,
		templateExamples: false,
	},
} as const;
