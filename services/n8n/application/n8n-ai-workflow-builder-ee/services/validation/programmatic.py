"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/programmatic.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation 的工作流校验。导入/依赖:外部:无；内部:n8n-workflow；本地:./types。导出:programmaticValidation。关键函数/方法:programmaticValidation。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/programmatic.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/validation/programmatic.py

import type { INodeTypeDescription } from 'n8n-workflow';

import {
	validateAgentPrompt,
	validateConnections,
	validateCredentials,
	validateFromAi,
	validateNodes,
	validateTools,
	validateTrigger,
} from '@/validation/checks';

import type { ProgrammaticChecksResult, ProgrammaticEvaluationInput } from './types';

export function programmaticValidation(
	input: ProgrammaticEvaluationInput,
	nodeTypes: INodeTypeDescription[],
): ProgrammaticChecksResult {
	const { generatedWorkflow } = input;

	const connectionsValidationResult = validateConnections(generatedWorkflow, nodeTypes);
	const nodesValidationResult = validateNodes(generatedWorkflow, nodeTypes);
	const triggerValidationResult = validateTrigger(generatedWorkflow, nodeTypes);
	const agentPromptValidationResult = validateAgentPrompt(generatedWorkflow);
	const toolsValidationResult = validateTools(generatedWorkflow, nodeTypes);
	const fromAiValidationResult = validateFromAi(generatedWorkflow, nodeTypes);
	const credentialsValidationResult = validateCredentials(generatedWorkflow);

	return {
		connections: connectionsValidationResult,
		nodes: nodesValidationResult,
		trigger: triggerValidationResult,
		agentPrompt: agentPromptValidationResult,
		tools: toolsValidationResult,
		fromAi: fromAiValidationResult,
		credentials: credentialsValidationResult,
	};
}
