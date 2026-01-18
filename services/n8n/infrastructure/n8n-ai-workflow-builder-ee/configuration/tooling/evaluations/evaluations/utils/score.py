"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/utils/score.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/utils 的工作流工具。导入/依赖:外部:无；内部:@/validation/types；本地:无。导出:calculateOverallScore、calcSingleEvaluatorScore。关键函数/方法:calculateOverallScore、calcSingleEvaluatorScore。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/utils/score.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/utils/score.py

import type { ProgrammaticEvaluationResult, SingleEvaluatorResult } from '@/validation/types';

export function calculateOverallScore(
	evaluatorResults: Omit<ProgrammaticEvaluationResult, 'overallScore'>,
): number {
	// Base weights for when similarity is not available
	const baseWeights = {
		connections: 0.25,
		trigger: 0.25,
		agentPrompt: 0.2,
		tools: 0.2,
		fromAi: 0.1,
	};

	// If similarity is available, adjust weights to include it
	let weights: Record<string, number>;
	let applicableCategories: string[];

	if (evaluatorResults.similarity) {
		// Rebalance weights to include similarity (20% weight)
		weights = {
			connections: 0.2,
			trigger: 0.2,
			agentPrompt: 0.16,
			tools: 0.16,
			fromAi: 0.08,
			similarity: 0.2,
		};
		applicableCategories = Object.keys(evaluatorResults).filter(
			(k) => k !== 'similarity' || evaluatorResults.similarity !== null,
		);
	} else {
		weights = baseWeights;
		applicableCategories = Object.keys(evaluatorResults).filter((k) => k !== 'similarity');
	}

	const total = applicableCategories.reduce((acc, category) => {
		const result = evaluatorResults[category as keyof typeof evaluatorResults];
		if (result && typeof result === 'object' && 'score' in result) {
			return acc + result.score * (weights[category] || 0);
		}
		return acc;
	}, 0);

	return total;
}

export function calcSingleEvaluatorScore(
	result: Pick<SingleEvaluatorResult, 'violations'>,
): number {
	const totalPointsDeducted = result.violations.reduce(
		(acc, violation) => acc + violation.pointsDeducted,
		0,
	);

	return Math.max(0, 100 - totalPointsDeducted) / 100;
}
