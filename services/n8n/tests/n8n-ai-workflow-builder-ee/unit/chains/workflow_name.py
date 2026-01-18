"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/chains/workflow-name.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/chains 的工作流模块。导入/依赖:外部:@langchain/core/…/chat_models、zod；内部:@/prompts/…/workflow-name.prompt；本地:无。导出:无。关键函数/方法:workflowNameChain、structuredOutput。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/chains/workflow-name.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/chains/workflow_name.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import z from 'zod';

import { workflowNamingPromptTemplate } from '@/prompts/chains/workflow-name.prompt';

export async function workflowNameChain(llm: BaseChatModel, initialPrompt: string) {
	// Use structured output for the workflow name to ensure it meets the required format and length
	const nameSchema = z.object({
		name: z.string().min(10).max(128).describe('Name of the workflow based on the prompt'),
	});

	const modelWithStructure = llm.withStructuredOutput(nameSchema);

	const prompt = await workflowNamingPromptTemplate.invoke({
		initialPrompt,
	});

	const structuredOutput = (await modelWithStructure.invoke(prompt)) as z.infer<typeof nameSchema>;

	return {
		name: structuredOutput.name,
	};
}
