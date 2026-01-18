"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/categorize-prompt.tool.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools 的工作流模块。导入/依赖:外部:@langchain/core/…/chat_models、@langchain/core/tools、zod；内部:@n8n/backend-common、@/chains/prompt-categorization、@/errors、@/tools/…/progress、@/tools/…/response、@/types/categorization 等2项；本地:无。导出:CATEGORIZE_PROMPT_TOOL、createCategorizePromptTool。关键函数/方法:buildCategorizationMessage、createCategorizePromptTool、async。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/categorize-prompt.tool.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/tools/categorize_prompt_tool.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import { tool } from '@langchain/core/tools';
import type { Logger } from '@n8n/backend-common';
import { z } from 'zod';

import { promptCategorizationChain } from '@/chains/prompt-categorization';
import { ValidationError, ToolExecutionError } from '@/errors';
import { createProgressReporter } from '@/tools/helpers/progress';
import { createSuccessResponse, createErrorResponse } from '@/tools/helpers/response';
import type { PromptCategorization } from '@/types/categorization';
import type { CategorizePromptOutput } from '@/types/tools';
import type { BuilderTool, BuilderToolBase } from '@/utils/stream-processor';

const categorizePromptSchema = z.object({
	prompt: z.string().min(1).describe('The user prompt to categorize'),
});

function buildCategorizationMessage(categorization: PromptCategorization): string {
	const parts: string[] = [];

	parts.push('Prompt categorized');

	if (categorization.techniques.length > 0) {
		parts.push(`- Techniques: ${categorization.techniques.join(', ')}`);
	}

	if (categorization.confidence !== undefined) {
		parts.push(`- Confidence: ${(categorization.confidence * 100).toFixed(0)}%`);
	}

	return parts.join('\n');
}

export const CATEGORIZE_PROMPT_TOOL: BuilderToolBase = {
	toolName: 'categorize_prompt',
	displayTitle: 'Categorizing prompt',
};

export function createCategorizePromptTool(llm: BaseChatModel, logger?: Logger): BuilderTool {
	const dynamicTool = tool(
		async (input, config) => {
			const reporter = createProgressReporter(
				config,
				CATEGORIZE_PROMPT_TOOL.toolName,
				CATEGORIZE_PROMPT_TOOL.displayTitle,
			);

			try {
				const validatedInput = categorizePromptSchema.parse(input);
				const { prompt } = validatedInput;

				reporter.start(validatedInput);

				logger?.debug('Categorizing user prompt using LLM...');
				reporter.progress('Analyzing prompt to identify use case and techniques...');

				const categorization = await promptCategorizationChain(llm, prompt);

				logger?.debug('Prompt categorized', {
					techniques: categorization.techniques,
					confidence: categorization.confidence,
				});

				const output: CategorizePromptOutput = {
					categorization,
				};
				reporter.complete(output);

				return createSuccessResponse(config, buildCategorizationMessage(categorization), {
					categorization,
					techniqueCategories: categorization.techniques,
				});
			} catch (error) {
				if (error instanceof z.ZodError) {
					const validationError = new ValidationError('Invalid input parameters', {
						extra: { errors: error.errors },
					});
					reporter.error(validationError);
					return createErrorResponse(config, validationError);
				}

				const toolError = new ToolExecutionError(
					error instanceof Error ? error.message : 'Unknown error occurred',
					{
						toolName: CATEGORIZE_PROMPT_TOOL.toolName,
						cause: error instanceof Error ? error : undefined,
					},
				);
				reporter.error(toolError);
				return createErrorResponse(config, toolError);
			}
		},
		{
			name: CATEGORIZE_PROMPT_TOOL.toolName,
			description: `Categorize a user's workflow request to identify the use case and required techniques.

This helps understand what type of workflow the user wants to build and which automation patterns will be needed.

Use this tool when you receive an initial workflow request to:
- Detect required techniques (e.g., scraping, data transformation, notifications)
- Better understand the user's needs and context

The categorization allows retrieving relevant best practice documentation to improve workflow structure and node selection.`,
			schema: categorizePromptSchema,
		},
	);

	return {
		tool: dynamicTool,
		...CATEGORIZE_PROMPT_TOOL,
	};
}
