"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/chains/evaluators/base.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/chains/evaluators 的工作流评估器。导入/依赖:外部:@langchain/core/…/chat_models、@langchain/core/messages、@langchain/core/prompts、@langchain/core/runnables、zod；内部:n8n-workflow；本地:../types/evaluation。导出:createEvaluatorChain。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/chains/evaluators/base.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/chains/evaluators/base.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import { SystemMessage } from '@langchain/core/messages';
import { ChatPromptTemplate, HumanMessagePromptTemplate } from '@langchain/core/prompts';
import type { Runnable, RunnableConfig } from '@langchain/core/runnables';
import { RunnableSequence } from '@langchain/core/runnables';
import { OperationalError } from 'n8n-workflow';
import type { z } from 'zod';

import type { EvaluationInput } from '../../types/evaluation';

type EvaluatorChainInput = {
	userPrompt: string;
	generatedWorkflow: string;
	referenceSection: string;
};

export function createEvaluatorChain<TResult extends Record<string, unknown>>(
	llm: BaseChatModel,
	schema: z.ZodType<TResult>,
	systemPrompt: string,
	humanTemplate: string,
): RunnableSequence<EvaluatorChainInput, TResult> {
	if (!llm.bindTools) {
		throw new OperationalError("LLM doesn't support binding tools");
	}

	const prompt = ChatPromptTemplate.fromMessages([
		new SystemMessage(systemPrompt),
		HumanMessagePromptTemplate.fromTemplate(humanTemplate),
	]);

	const llmWithStructuredOutput = llm.withStructuredOutput<TResult>(schema);

	return RunnableSequence.from<EvaluatorChainInput, TResult>([prompt, llmWithStructuredOutput]);
}

export async function invokeEvaluatorChain<TResult>(
	chain: Runnable<EvaluatorChainInput, TResult>,
	input: EvaluationInput,
	config?: RunnableConfig,
): Promise<TResult> {
	const referenceSection = input.referenceWorkflow
		? `<reference_workflow>\n${JSON.stringify(input.referenceWorkflow, null, 2)}\n</reference_workflow>`
		: '';

	const result = await chain.invoke(
		{
			userPrompt: input.userPrompt,
			generatedWorkflow: JSON.stringify(input.generatedWorkflow, null, 2),
			referenceSection,
		},
		config,
	);

	return result;
}
