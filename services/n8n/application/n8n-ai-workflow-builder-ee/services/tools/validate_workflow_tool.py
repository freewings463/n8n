"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/validate-workflow.tool.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools 的工作流模块。导入/依赖:外部:@langchain/core/tools、zod；内部:@n8n/backend-common、n8n-workflow 等3项；本地:../errors、../utils/workflow-validation、./helpers/progress、./helpers/response 等1项。导出:VALIDATE_WORKFLOW_TOOL、createValidateWorkflowTool。关键函数/方法:collectValidationResultForTelemetry、createValidateWorkflowTool、async、reportProgress。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/validate-workflow.tool.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/validate_workflow_tool.py

import { tool } from '@langchain/core/tools';
import type { Logger } from '@n8n/backend-common';
import type { INodeTypeDescription } from 'n8n-workflow';
import { z } from 'zod';

import type { BuilderTool, BuilderToolBase } from '@/utils/stream-processor';
import { programmaticValidation } from '@/validation/programmatic';
import type {
	ProgrammaticViolation,
	ProgrammaticChecksResult,
	TelemetryValidationStatus,
} from '@/validation/types';
import { PROGRAMMATIC_VIOLATION_NAMES } from '@/validation/types';

import { ToolExecutionError, ValidationError } from '../errors';
import { formatWorkflowValidation } from '../utils/workflow-validation';
import { createProgressReporter, reportProgress } from './helpers/progress';
import { createErrorResponse, createSuccessResponse } from './helpers/response';
import { getWorkflowState } from './helpers/state';

const validateWorkflowSchema = z.object({}).strict().default({});

export const VALIDATE_WORKFLOW_TOOL: BuilderToolBase = {
	toolName: 'validate_workflow',
	displayTitle: 'Validating workflow',
};

/**
 * Creates a compacted validation result for use in telemetry
 * @returns `{ X: 'pass' | 'fail', Y: 'pass' | 'fail', ... }`
 */
function collectValidationResultForTelemetry(
	results: ProgrammaticChecksResult,
): TelemetryValidationStatus {
	const status = Object.fromEntries(
		PROGRAMMATIC_VIOLATION_NAMES.map((name) => [name, 'pass' as const]),
	) as TelemetryValidationStatus;

	Object.values(results).forEach((violations: ProgrammaticViolation[]) => {
		violations?.forEach((violation) => {
			status[violation.name] = 'fail';
		});
	});

	return status;
}

export function createValidateWorkflowTool(
	parsedNodeTypes: INodeTypeDescription[],
	logger?: Logger,
): BuilderTool {
	const dynamicTool = tool(
		async (input, config) => {
			const reporter = createProgressReporter(
				config,
				VALIDATE_WORKFLOW_TOOL.toolName,
				VALIDATE_WORKFLOW_TOOL.displayTitle,
			);

			try {
				const validatedInput = validateWorkflowSchema.parse(input ?? {});
				reporter.start(validatedInput);

				const state = getWorkflowState();
				reportProgress(reporter, 'Running programmatic checks');

				const violations = programmaticValidation(
					{
						generatedWorkflow: state.workflowJSON,
					},
					parsedNodeTypes,
				);

				const validationResultForTelemetry = collectValidationResultForTelemetry(violations);

				const message = formatWorkflowValidation(violations);

				reporter.complete({ message });

				return createSuccessResponse(config, message, {
					workflowValidation: violations,
					validationHistory: [validationResultForTelemetry],
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
					error instanceof Error ? error.message : 'Failed to validate workflow',
					{
						toolName: VALIDATE_WORKFLOW_TOOL.toolName,
						cause: error instanceof Error ? error : undefined,
					},
				);

				logger?.warn('validate_workflow tool failed', { error: toolError });

				reporter.error(toolError);
				return createErrorResponse(config, toolError);
			}
		},
		{
			name: VALIDATE_WORKFLOW_TOOL.toolName,
			description:
				'Run validation checks against the current workflow. Call this after making changes to ensure the workflow is valid.',
			schema: validateWorkflowSchema,
		},
	);

	return {
		tool: dynamicTool,
		...VALIDATE_WORKFLOW_TOOL,
	};
}
