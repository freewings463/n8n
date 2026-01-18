"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow.formatter.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/workflows 的工作流模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:formatWorkflow。关键函数/方法:formatWorkflow。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow.formatter.ts -> services/n8n/application/cli/services/workflows/workflow_formatter.py

import type { IWorkflowBase } from 'n8n-workflow';

/**
 * Display a workflow in a user-friendly format
 */
export function formatWorkflow(workflow: IWorkflowBase) {
	return `"${workflow.name}" (ID: ${workflow.id})`;
}
