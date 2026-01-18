"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/workflow-validation.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:无；内部:@/validation/types；本地:无。导出:formatWorkflowValidation。关键函数/方法:formatViolationsByCategory、formatWorkflowValidation。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/workflow-validation.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/workflow_validation.py

import type { ProgrammaticChecksResult, ProgrammaticViolation } from '@/validation/types';

function formatViolationsByCategory(
	categories: Array<[string, ProgrammaticViolation[]]>,
): string[] {
	const lines: string[] = [];

	for (const [name, violations] of categories) {
		if (!violations.length) continue;

		lines.push(`${name}:`);
		for (const violation of violations) {
			lines.push(`- (${violation.type}) ${violation.description}`);
		}
	}

	return lines;
}

export function formatWorkflowValidation(validation: ProgrammaticChecksResult | null): string {
	if (!validation) {
		return 'Workflow validation not yet run. Call the validate_workflow tool to analyze the current workflow.';
	}

	const lines: string[] = ['Workflow Validation Summary:'];

	const violationLines = formatViolationsByCategory([
		['Connections', validation.connections],
		['Trigger', validation.trigger],
		['Nodes', validation.nodes],
		['Agent Prompt', validation.agentPrompt],
		['Tools', validation.tools],
		['From AI', validation.fromAi],
	]);

	if (violationLines.length === 0) {
		lines.push('No validation violations detected.');
	} else {
		lines.push(...violationLines);
	}

	return lines.join('\n');
}
