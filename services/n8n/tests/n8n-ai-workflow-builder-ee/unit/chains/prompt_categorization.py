"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/chains/prompt-categorization.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/chains 的工作流模块。导入/依赖:外部:@langchain/core/…/chat_models、zod；内部:@/types/categorization；本地:无。导出:无。关键函数/方法:promptCategorizationChain。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/chains/prompt-categorization.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/chains/prompt_categorization.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import { z } from 'zod';

import {
	formatTechniqueList,
	promptCategorizationTemplate,
} from '@/prompts/chains/categorization.prompt';
import { WorkflowTechnique, type PromptCategorization } from '@/types/categorization';

export async function promptCategorizationChain(
	llm: BaseChatModel,
	userPrompt: string,
): Promise<PromptCategorization> {
	const categorizationSchema = z.object({
		techniques: z
			.array(z.nativeEnum(WorkflowTechnique))
			.min(0)
			.max(5)
			.describe('Zero to five workflow techniques identified in the prompt (maximum of 5)'),
		confidence: z
			.number()
			.min(0)
			.max(1)
			.describe('Confidence level in this categorization from 0.0 to 1.0'),
	});

	const modelWithStructure = llm.withStructuredOutput<PromptCategorization>(categorizationSchema);

	const prompt = await promptCategorizationTemplate.invoke({
		userPrompt,
		techniques: formatTechniqueList(),
	});

	const structuredOutput = await modelWithStructure.invoke(prompt);

	return {
		techniques: structuredOutput.techniques,
		confidence: structuredOutput.confidence,
	};
}
