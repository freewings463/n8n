"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/trim-workflow-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:无；内部:n8n-workflow、@/constants、@/types、@/utils/token-usage；本地:无。导出:trimWorkflowJSON。关键函数/方法:trimParameterValue、trimWorkflowJsonWithThreshold、trimWorkflowJSON。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/trim-workflow-context.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/trim_workflow_context.py

import type { INodeParameters, NodeParameterValueType } from 'n8n-workflow';

import { MAX_WORKFLOW_LENGTH_TOKENS } from '@/constants';
import type { SimpleWorkflow } from '@/types';
import { estimateTokenCountFromString } from '@/utils/token-usage';

/**
 * Thresholds for progressively trimming large parameter values.
 * Each iteration uses a more aggressive threshold if the workflow is still too large.
 */
const MAX_PARAMETER_VALUE_LENGTH_THRESHOLDS = [10000, 5000, 2000, 1000];

/**
 * Trims a parameter value if it exceeds the specified threshold.
 * Replaces large values with placeholders to reduce token usage.
 *
 * @param value - The parameter value to potentially trim
 * @param threshold - The maximum allowed length in characters
 * @returns The original value if under threshold, or a placeholder string if too large
 */
function trimParameterValue(
	value: NodeParameterValueType,
	threshold: number,
): NodeParameterValueType {
	// Handle undefined and null values directly without stringification
	if (value === undefined || value === null) {
		return value;
	}

	const valueStr = JSON.stringify(value);
	if (valueStr.length > threshold) {
		// Return type-specific placeholder messages
		if (typeof value === 'string') {
			return '[Large value omitted]';
		} else if (Array.isArray(value)) {
			return '[Large array omitted]';
		} else if (typeof value === 'object' && value !== null) {
			return '[Large object omitted]';
		}
	}

	return value;
}

/**
 * Simplifies a workflow by trimming large parameter values of its nodes based on the given threshold.
 * Creates a copy of the workflow to avoid mutations.
 *
 * @param workflow - The workflow to simplify
 * @param threshold - The maximum allowed length for parameter values
 * @returns A new workflow object with trimmed parameters
 */
function trimWorkflowJsonWithThreshold(
	workflow: SimpleWorkflow,
	threshold: number,
): SimpleWorkflow {
	const simplifiedWorkflow = { ...workflow };
	if (simplifiedWorkflow.nodes) {
		simplifiedWorkflow.nodes = simplifiedWorkflow.nodes.map((node) => {
			const simplifiedNode = { ...node };

			// Process each parameter and replace large values with placeholders
			if (simplifiedNode.parameters) {
				const simplifiedParameters: INodeParameters = {};
				for (const [key, value] of Object.entries(simplifiedNode.parameters)) {
					simplifiedParameters[key] = trimParameterValue(value, threshold);
				}
				simplifiedNode.parameters = simplifiedParameters;
			}

			return simplifiedNode;
		});
	}

	return simplifiedWorkflow;
}

/**
 * Trims workflow JSON to fit within token limits by progressively applying more aggressive trimming.
 * Iterates through different thresholds until the workflow fits within MAX_WORKFLOW_LENGTH_TOKENS.
 *
 * @param workflow - The workflow to trim
 * @returns A simplified workflow that fits within token limits, or the most aggressively trimmed version
 */
export function trimWorkflowJSON(workflow: SimpleWorkflow): SimpleWorkflow {
	// Try progressively more aggressive trimming thresholds
	for (const threshold of MAX_PARAMETER_VALUE_LENGTH_THRESHOLDS) {
		const simplified = trimWorkflowJsonWithThreshold(workflow, threshold);
		const workflowStr = JSON.stringify(simplified);
		const estimatedTokens = estimateTokenCountFromString(workflowStr);

		// If the workflow fits within the token limit, return it
		if (estimatedTokens <= MAX_WORKFLOW_LENGTH_TOKENS) {
			return simplified;
		}
	}

	// If even the most aggressive trimming doesn't fit, return the most trimmed version
	// This ensures we always return something, even if it still exceeds the limit
	return trimWorkflowJsonWithThreshold(
		workflow,
		MAX_PARAMETER_VALUE_LENGTH_THRESHOLDS[MAX_PARAMETER_VALUE_LENGTH_THRESHOLDS.length - 1],
	);
}
