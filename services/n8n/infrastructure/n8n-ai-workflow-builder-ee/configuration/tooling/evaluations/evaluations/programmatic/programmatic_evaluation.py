"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/programmatic/programmatic-evaluation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/programmatic 的工作流模块。导入/依赖:外部:无；内部:n8n-workflow、@/validation/types；本地:../utils/score。导出:无。关键函数/方法:programmaticEvaluation。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/programmatic/programmatic-evaluation.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/programmatic/programmatic_evaluation.py

import type { INodeTypeDescription } from 'n8n-workflow';

import type { ProgrammaticEvaluationInput, ProgrammaticViolation } from '@/validation/types';

import {
	evaluateConnections,
	evaluateCredentials,
	evaluateNodes,
	evaluateTools,
	evaluateAgentPrompt,
	evaluateFromAi,
	evaluateTrigger,
} from './evaluators';
import {
	evaluateWorkflowSimilarity,
	evaluateWorkflowSimilarityMultiple,
} from './evaluators/workflow-similarity';
import { calculateOverallScore } from '../utils/score';

export async function programmaticEvaluation(
	input: ProgrammaticEvaluationInput,
	nodeTypes: INodeTypeDescription[],
) {
	const { generatedWorkflow, referenceWorkflow, referenceWorkflows, preset = 'standard' } = input;

	const connectionsEvaluationResult = evaluateConnections(generatedWorkflow, nodeTypes);
	const nodesEvaluationResult = evaluateNodes(generatedWorkflow, nodeTypes);
	const triggerEvaluationResult = evaluateTrigger(generatedWorkflow, nodeTypes);
	const agentPromptEvaluationResult = evaluateAgentPrompt(generatedWorkflow);
	const toolsEvaluationResult = evaluateTools(generatedWorkflow, nodeTypes);
	const fromAiEvaluationResult = evaluateFromAi(generatedWorkflow, nodeTypes);
	const credentialsEvaluationResult = evaluateCredentials(generatedWorkflow);

	// Workflow similarity evaluation (supports both single and multiple reference workflows)
	let similarityEvaluationResult = null;

	// Prioritize referenceWorkflows (multiple) over referenceWorkflow (single)
	if (referenceWorkflows && referenceWorkflows.length > 0) {
		try {
			similarityEvaluationResult = await evaluateWorkflowSimilarityMultiple(
				generatedWorkflow,
				referenceWorkflows,
				preset,
			);
		} catch (error) {
			console.warn('Multiple workflow similarity evaluation failed:', error);
			// Fallback to neutral result if similarity check fails
			const violation: ProgrammaticViolation = {
				name: 'workflow-similarity-evaluation-failed',
				type: 'critical',
				description: `Similarity evaluation failed: ${(error as Error).message}`,
				pointsDeducted: 0,
			};
			similarityEvaluationResult = {
				violations: [violation],
				score: 0,
			};
		}
	} else if (referenceWorkflow) {
		try {
			similarityEvaluationResult = await evaluateWorkflowSimilarity(
				generatedWorkflow,
				referenceWorkflow,
				preset,
			);
		} catch (error) {
			console.warn('Workflow similarity evaluation failed:', error);
			// Fallback to neutral result if similarity check fails
			const violation: ProgrammaticViolation = {
				name: 'workflow-similarity-evaluation-failed',
				type: 'critical',
				description: `Similarity evaluation failed: ${(error as Error).message}`,
				pointsDeducted: 0,
			};
			similarityEvaluationResult = {
				violations: [violation],
				score: 0,
			};
		}
	}

	const overallScore = calculateOverallScore({
		connections: connectionsEvaluationResult,
		nodes: nodesEvaluationResult,
		trigger: triggerEvaluationResult,
		agentPrompt: agentPromptEvaluationResult,
		tools: toolsEvaluationResult,
		fromAi: fromAiEvaluationResult,
		credentials: credentialsEvaluationResult,
		similarity: similarityEvaluationResult,
	});

	return {
		overallScore,
		connections: connectionsEvaluationResult,
		nodes: nodesEvaluationResult,
		trigger: triggerEvaluationResult,
		agentPrompt: agentPromptEvaluationResult,
		tools: toolsEvaluationResult,
		fromAi: fromAiEvaluationResult,
		credentials: credentialsEvaluationResult,
		similarity: similarityEvaluationResult,
	};
}
