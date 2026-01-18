"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/pairwise/generator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/pairwise 的工作流模块。导入/依赖:外部:@langchain/core/…/chat_models、langsmith/evaluation、langsmith/traceable；内部:n8n-workflow；本地:./judge-panel、./metrics-builder、./types、../types/workflow 等5项。导出:CreatePairwiseTargetOptions、createPairwiseTarget。关键函数/方法:createPairwiseTarget、async、generateWorkflow、getChatPayload。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/pairwise/generator.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/pairwise/generator.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import type { EvaluationResult as LangsmithEvaluationResult } from 'langsmith/evaluation';
import { traceable } from 'langsmith/traceable';
import type { INodeTypeDescription } from 'n8n-workflow';

import { runJudgePanel, aggregateGenerations, type GenerationResult } from './judge-panel';
import { buildSingleGenerationResults, buildMultiGenerationResults } from './metrics-builder';
import type { PairwiseDatasetInput, PairwiseTargetOutput } from './types';
import type { SimpleWorkflow } from '../../src/types/workflow';
import type { BuilderFeatureFlags } from '../../src/workflow-builder-agent';
import { EVAL_TYPES, EVAL_USERS, TRACEABLE_NAMES } from '../constants';
import { createAgent } from '../core/environment';
import { generateRunId, isWorkflowStateValues } from '../types/langsmith';
import { consumeGenerator, getChatPayload } from '../utils/evaluation-helpers';

// ============================================================================
// Target Factory
// ============================================================================

export interface CreatePairwiseTargetOptions {
	parsedNodeTypes: INodeTypeDescription[];
	llm: BaseChatModel;
	numJudges: number;
	numGenerations: number;
	featureFlags?: BuilderFeatureFlags;
	experimentName?: string;
}

/**
 * Creates a target function that does ALL the work:
 * - Generates all workflows (each wrapped in traceable)
 * - Runs judge panels
 * - Returns pre-computed feedback
 *
 * The evaluator then just extracts the pre-computed feedback.
 * This avoids 403 errors from nested traceable in evaluator context.
 */
export function createPairwiseTarget(options: CreatePairwiseTargetOptions) {
	const { parsedNodeTypes, llm, numJudges, numGenerations, featureFlags, experimentName } = options;

	return traceable(
		async (inputs: PairwiseDatasetInput): Promise<PairwiseTargetOutput> => {
			const { prompt, evals: evalCriteria } = inputs;

			// Generate ALL workflows and run judges in parallel
			const generationResults: GenerationResult[] = await Promise.all(
				Array.from({ length: numGenerations }, async (_, i) => {
					const generationIndex = i + 1;
					// Wrap each generation in traceable for proper visibility
					const generate = traceable(
						async () => await generateWorkflow(parsedNodeTypes, llm, prompt, featureFlags),
						{
							name: `generation_${generationIndex}`,
							run_type: 'chain',
							metadata: {
								...(experimentName && { experiment_name: experimentName }),
							},
						},
					);
					const workflow = await generate();
					const panelResult = await runJudgePanel(llm, workflow, evalCriteria, numJudges, {
						generationIndex,
						experimentName,
					});
					return { workflow, ...panelResult };
				}),
			);

			if (numGenerations === 1) {
				const singleGenFeedback = buildSingleGenerationResults(generationResults[0], numJudges);
				return { prompt, evals: evalCriteria, feedback: singleGenFeedback };
			}

			const aggregation = aggregateGenerations(generationResults);
			const multiGenFeedback: LangsmithEvaluationResult[] = buildMultiGenerationResults(
				aggregation,
				numJudges,
			);

			return { prompt, evals: evalCriteria, feedback: multiGenFeedback };
		},
		{ name: TRACEABLE_NAMES.PAIRWISE_EVALUATION, run_type: 'chain' },
	);
}

/**
 * Generate a single workflow.
 * Used for local evaluation and regeneration in multi-generation mode.
 */
export async function generateWorkflow(
	parsedNodeTypes: INodeTypeDescription[],
	llm: BaseChatModel,
	prompt: string,
	featureFlags?: BuilderFeatureFlags,
): Promise<SimpleWorkflow> {
	const runId = generateRunId();

	const agent = createAgent({ parsedNodeTypes, llm, featureFlags });

	await consumeGenerator(
		agent.chat(
			getChatPayload({
				evalType: EVAL_TYPES.PAIRWISE_LOCAL,
				message: prompt,
				workflowId: runId,
				featureFlags,
			}),
			EVAL_USERS.PAIRWISE_LOCAL,
		),
	);

	const state = await agent.getState(runId, EVAL_USERS.PAIRWISE_LOCAL);

	if (!state.values || !isWorkflowStateValues(state.values)) {
		throw new Error('Invalid workflow state: workflow or messages missing');
	}

	return state.values.workflowJSON;
}
