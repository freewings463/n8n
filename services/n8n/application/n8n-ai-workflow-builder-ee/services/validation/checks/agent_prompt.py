"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/agent-prompt.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation/checks 的工作流校验。导入/依赖:外部:无；内部:n8n-workflow、@/types；本地:../types、../utils/expressions。导出:validateAgentPrompt。关键函数/方法:isOptionsWithSystemMessage、validateAgentPrompt。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/agent-prompt.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/validation/checks/agent_prompt.py

import type { INodeParameters } from 'n8n-workflow';

import type { SimpleWorkflow } from '@/types';

import type { ProgrammaticViolation } from '../types';
import { containsExpression } from '../utils/expressions';

/**
 * Type guard to check if a value is a valid options object with systemMessage
 */
function isOptionsWithSystemMessage(
	value: unknown,
): value is { systemMessage?: string } & INodeParameters {
	return (
		typeof value === 'object' &&
		value !== null &&
		!Array.isArray(value) &&
		('systemMessage' in value || Object.keys(value).length === 0)
	);
}

/**
 * Evaluates Agent nodes to ensure:
 * 1. Their prompts contain expressions (for dynamic context)
 * 2. They have a system message defined
 * Agent nodes without expressions in prompts (e.g., that failed to use chatInput
 * when there was a chat trigger) are most probably errors.
 */
export function validateAgentPrompt(workflow: SimpleWorkflow): ProgrammaticViolation[] {
	const violations: ProgrammaticViolation[] = [];

	// Check if workflow has nodes
	if (!workflow.nodes || workflow.nodes.length === 0) {
		return [];
	}

	// Find all agent nodes and check their prompts
	for (const node of workflow.nodes) {
		// Check if this is an Agent node (ToolsAgent)
		if (node.type === '@n8n/n8n-nodes-langchain.agent') {
			// Check the text parameter for expressions
			const textParam = node.parameters?.text;
			const promptType = node.parameters?.promptType;
			const options = node.parameters?.options;

			// Use type guard to safely access systemMessage
			let systemMessage: string | undefined;
			if (isOptionsWithSystemMessage(options)) {
				systemMessage = options.systemMessage;
			}

			// Only check when promptType is 'define' or undefined (default)
			// 'auto' mode means it uses text from previous node
			if (promptType !== 'auto' && promptType !== 'guardrails') {
				// Check 1: Text parameter should contain expressions for dynamic context
				if (!textParam || !containsExpression(textParam)) {
					violations.push({
						name: 'agent-static-prompt',
						type: 'major',
						description: `Agent node "${node.name}" has no expression in its prompt field. This likely means it failed to use chatInput or dynamic context`,
						pointsDeducted: 20,
					});
				}

				// Check 2: Agent should have a system message
				// If systemMessage is missing, it likely means all instructions are in the text field
				if (!systemMessage || systemMessage.trim().length === 0) {
					violations.push({
						name: 'agent-no-system-prompt',
						type: 'major',
						description: `Agent node "${node.name}" has no system message. System-level instructions (role, tasks, behavior) should be in the system message field, not the text field`,
						pointsDeducted: 25,
					});
				}
			}
		}
	}

	return violations;
}
