"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/validate-configuration.tool.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools 的工作流模块。导入/依赖:外部:@langchain/core/tools、zod；内部:n8n-workflow、@/utils/stream-processor、@/validation/checks；本地:../errors、./helpers/progress、./helpers/response、./helpers/state。导出:VALIDATE_CONFIGURATION_TOOL、createValidateConfigurationTool。关键函数/方法:createValidateConfigurationTool、async、reportProgress。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/validate-configuration.tool.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/validate_configuration_tool.py

import { tool } from '@langchain/core/tools';
import type { INodeTypeDescription } from 'n8n-workflow';
import { z } from 'zod';

import type { BuilderTool, BuilderToolBase } from '@/utils/stream-processor';
import { validateAgentPrompt, validateTools, validateFromAi } from '@/validation/checks';

import { ToolExecutionError, ValidationError } from '../errors';
import { createProgressReporter, reportProgress } from './helpers/progress';
import { createErrorResponse, createSuccessResponse } from './helpers/response';
import { getWorkflowState } from './helpers/state';

const validateConfigurationSchema = z.object({}).strict().default({});

export const VALIDATE_CONFIGURATION_TOOL: BuilderToolBase = {
	toolName: 'validate_configuration',
	displayTitle: 'Validating configuration',
};

/**
 * Validation tool for Configurator subgraph.
 * Checks node configuration: agent prompts, tool parameters, $fromAI usage.
 */
export function createValidateConfigurationTool(
	parsedNodeTypes: INodeTypeDescription[],
): BuilderTool {
	const dynamicTool = tool(
		async (input, config) => {
			const reporter = createProgressReporter(
				config,
				VALIDATE_CONFIGURATION_TOOL.toolName,
				VALIDATE_CONFIGURATION_TOOL.displayTitle,
			);

			try {
				const validatedInput = validateConfigurationSchema.parse(input ?? {});
				reporter.start(validatedInput);

				const state = getWorkflowState();
				reportProgress(reporter, 'Validating configuration');

				const agentViolations = validateAgentPrompt(state.workflowJSON);
				const toolViolations = validateTools(state.workflowJSON, parsedNodeTypes);
				const fromAiViolations = validateFromAi(state.workflowJSON, parsedNodeTypes);

				const allViolations = [...agentViolations, ...toolViolations, ...fromAiViolations];

				let message: string;
				if (allViolations.length === 0) {
					message = 'Configuration is valid. Agent prompts, tools, and $fromAI usage are correct.';
				} else {
					message = `Found ${allViolations.length} configuration issues:\n${allViolations.map((v) => `- ${v.description}`).join('\n')}`;
				}

				reporter.complete({ message });

				return createSuccessResponse(config, message, {
					configurationValidation: {
						agentPrompt: agentViolations,
						tools: toolViolations,
						fromAi: fromAiViolations,
					},
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
					error instanceof Error ? error.message : 'Failed to validate configuration',
					{
						toolName: VALIDATE_CONFIGURATION_TOOL.toolName,
						cause: error instanceof Error ? error : undefined,
					},
				);

				reporter.error(toolError);
				return createErrorResponse(config, toolError);
			}
		},
		{
			name: VALIDATE_CONFIGURATION_TOOL.toolName,
			description:
				'Validate node configuration (agent prompts, tool parameters, $fromAI usage). Call after configuring nodes to check for issues.',
			schema: validateConfigurationSchema,
		},
	);

	return {
		tool: dynamicTool,
		...VALIDATE_CONFIGURATION_TOOL,
	};
}
