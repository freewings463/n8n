"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/get-best-practices.tool.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools 的工作流模块。导入/依赖:外部:@langchain/core/tools、zod；内部:@/errors、@/tools/best-practices、@/tools/…/progress、@/tools/…/response、@/types/categorization、@/utils/stream-processor；本地:无。导出:GET_BEST_PRACTICES_TOOL、createGetBestPracticesTool。关键函数/方法:formatBestPractices、createGetBestPracticesTool。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/get-best-practices.tool.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/tools/get_best_practices_tool.py

import { tool } from '@langchain/core/tools';
import { z } from 'zod';

import { ValidationError, ToolExecutionError } from '@/errors';
import { documentation } from '@/tools/best-practices';
import { createProgressReporter } from '@/tools/helpers/progress';
import { createSuccessResponse, createErrorResponse } from '@/tools/helpers/response';
import { WorkflowTechnique, type WorkflowTechniqueType } from '@/types/categorization';
import type { BuilderToolBase } from '@/utils/stream-processor';

const getBestPracticesSchema = z.object({
	techniques: z
		.array(z.nativeEnum(WorkflowTechnique))
		.min(1)
		.describe('List of workflow techniques to retrieve best practices for'),
});

/**
 * Format best practices documentation for multiple techniques
 */
function formatBestPractices(techniques: WorkflowTechniqueType[]): string {
	const parts: string[] = [];
	const foundDocs: string[] = [];

	for (const technique of techniques) {
		const doc = documentation[technique];
		if (doc) {
			foundDocs.push(doc.getDocumentation());
		}
	}

	if (foundDocs.length > 0) {
		parts.push('<best_practices>');
		parts.push(foundDocs.join('\n---\n'));
		parts.push('</best_practices>');
	}

	return parts.join('\n');
}

export const GET_BEST_PRACTICES_TOOL: BuilderToolBase = {
	toolName: 'get_best_practices',
	displayTitle: 'Getting best practices',
};

/**
 * Factory function to create the get best practices tool
 */
export function createGetBestPracticesTool() {
	const dynamicTool = tool(
		(input: unknown, config) => {
			const reporter = createProgressReporter(
				config,
				GET_BEST_PRACTICES_TOOL.toolName,
				GET_BEST_PRACTICES_TOOL.displayTitle,
			);

			try {
				const validatedInput = getBestPracticesSchema.parse(input);
				const { techniques } = validatedInput;

				reporter.start(validatedInput);

				reporter.progress(`Retrieving best practices for ${techniques.length} technique(s)...`);

				// Get available documentation
				const availableDocs = techniques.filter((technique) => documentation[technique]);

				if (availableDocs.length === 0) {
					const message = `No best practices documentation available for the requested techniques: ${techniques.join(', ')}`;
					reporter.complete({ techniques, found: 0 });
					return createSuccessResponse(config, message);
				}

				// Format the documentation
				const message = formatBestPractices(techniques);

				reporter.complete({
					techniques,
					found: availableDocs.length,
					missing: techniques.length - availableDocs.length,
				});

				return createSuccessResponse(config, message);
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
						toolName: GET_BEST_PRACTICES_TOOL.toolName,
						cause: error instanceof Error ? error : undefined,
					},
				);
				reporter.error(toolError);
				return createErrorResponse(config, toolError);
			}
		},
		{
			name: GET_BEST_PRACTICES_TOOL.toolName,
			description: `Retrieve best practices documentation for specific workflow techniques.

Use this tool after categorizing a user's prompt to get relevant guidance on:
- Recommended nodes and their purposes
- Common pitfalls to avoid
- Performance and resource management tips
- Implementation patterns and best practices
- General tips on building workflows that utilise the provided techniques

This helps build better workflows by applying proven patterns and avoiding common mistakes.`,
			schema: getBestPracticesSchema,
		},
	);

	return {
		tool: dynamicTool,
		...GET_BEST_PRACTICES_TOOL,
	};
}
