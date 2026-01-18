"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/validate-structure.tool.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools 的工作流模块。导入/依赖:外部:@langchain/core/tools、zod；内部:n8n-workflow、@/utils/stream-processor、@/validation/checks；本地:../errors、./helpers/progress、./helpers/response、./helpers/state。导出:VALIDATE_STRUCTURE_TOOL、createValidateStructureTool。关键函数/方法:createValidateStructureTool、async、reportProgress。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/validate-structure.tool.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/validate_structure_tool.py

import { tool } from '@langchain/core/tools';
import type { INodeTypeDescription } from 'n8n-workflow';
import { z } from 'zod';

import type { BuilderTool, BuilderToolBase } from '@/utils/stream-processor';
import { validateConnections, validateTrigger } from '@/validation/checks';

import { ToolExecutionError, ValidationError } from '../errors';
import { createProgressReporter, reportProgress } from './helpers/progress';
import { createErrorResponse, createSuccessResponse } from './helpers/response';
import { getWorkflowState } from './helpers/state';

const validateStructureSchema = z.object({}).strict().default({});

export const VALIDATE_STRUCTURE_TOOL: BuilderToolBase = {
	toolName: 'validate_structure',
	displayTitle: 'Validating structure',
};

/**
 * Validation tool for Builder subgraph.
 * Checks workflow structure: connections and trigger presence.
 */
export function createValidateStructureTool(parsedNodeTypes: INodeTypeDescription[]): BuilderTool {
	const dynamicTool = tool(
		async (input, config) => {
			const reporter = createProgressReporter(
				config,
				VALIDATE_STRUCTURE_TOOL.toolName,
				VALIDATE_STRUCTURE_TOOL.displayTitle,
			);

			try {
				const validatedInput = validateStructureSchema.parse(input ?? {});
				reporter.start(validatedInput);

				const state = getWorkflowState();
				reportProgress(reporter, 'Validating structure');

				const connectionViolations = validateConnections(state.workflowJSON, parsedNodeTypes);
				const triggerViolations = validateTrigger(state.workflowJSON, parsedNodeTypes);

				const allViolations = [...connectionViolations, ...triggerViolations];

				let message: string;
				if (allViolations.length === 0) {
					message =
						'Workflow structure is valid. All connections are correct and trigger node is present.';
				} else {
					message = `Found ${allViolations.length} structure issues:\n${allViolations.map((v) => `- ${v.description}`).join('\n')}`;
				}

				reporter.complete({ message });

				return createSuccessResponse(config, message, {
					structureValidation: { connections: connectionViolations, trigger: triggerViolations },
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
					error instanceof Error ? error.message : 'Failed to validate structure',
					{
						toolName: VALIDATE_STRUCTURE_TOOL.toolName,
						cause: error instanceof Error ? error : undefined,
					},
				);

				reporter.error(toolError);
				return createErrorResponse(config, toolError);
			}
		},
		{
			name: VALIDATE_STRUCTURE_TOOL.toolName,
			description:
				'Validate workflow structure (connections, trigger). Call after creating nodes/connections to check for issues.',
			schema: validateStructureSchema,
		},
	);

	return {
		tool: dynamicTool,
		...VALIDATE_STRUCTURE_TOOL,
	};
}
