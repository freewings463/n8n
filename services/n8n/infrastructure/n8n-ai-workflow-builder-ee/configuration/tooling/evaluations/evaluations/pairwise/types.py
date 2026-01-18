"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/pairwise/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/pairwise 的工作流类型。导入/依赖:外部:langsmith/evaluation、langsmith/schemas；内部:无；本地:无。导出:EvalCriteria、PairwiseDatasetInput、PairwiseExample、PairwiseTargetOutput、isPairwiseTargetOutput、isPairwiseExample。关键函数/方法:isPairwiseTargetOutput、isPairwiseExample。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/pairwise/types.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/pairwise/types.py

import type { EvaluationResult as LangsmithEvaluationResult } from 'langsmith/evaluation';
import type { Example } from 'langsmith/schemas';

// ============================================================================
// Evaluation Criteria
// ============================================================================

/** Evaluation criteria requiring at least one of dos or donts */
export type EvalCriteria = { dos: string; donts?: string } | { dos?: string; donts: string };

// ============================================================================
// Dataset Input/Output Types
// ============================================================================

export interface PairwiseDatasetInput {
	evals: EvalCriteria;
	prompt: string;
}

/** LangSmith Example with typed inputs for pairwise evaluation */
export interface PairwiseExample extends Omit<Example, 'inputs'> {
	inputs: PairwiseDatasetInput;
}

export interface PairwiseTargetOutput {
	prompt: string;
	evals: EvalCriteria;
	/** Pre-computed feedback results */
	feedback: LangsmithEvaluationResult[];
}

// ============================================================================
// Type Guards
// ============================================================================

export function isPairwiseTargetOutput(outputs: unknown): outputs is PairwiseTargetOutput {
	if (!outputs || typeof outputs !== 'object') return false;
	const obj = outputs as Record<string, unknown>;
	return (
		typeof obj.prompt === 'string' &&
		Array.isArray(obj.feedback) &&
		obj.evals !== undefined &&
		typeof obj.evals === 'object'
	);
}

export function isPairwiseExample(example: Example): example is PairwiseExample {
	const inputs = example.inputs as Record<string, unknown> | undefined;
	if (!inputs || typeof inputs !== 'object') return false;

	const evals = inputs.evals as Record<string, unknown> | undefined;
	if (!evals || typeof evals !== 'object') return false;

	return (
		typeof inputs.prompt === 'string' &&
		(typeof evals.dos === 'string' || typeof evals.donts === 'string')
	);
}
