"""
MIGRATION-META:
  source_path: packages/core/src/errors/workflow-has-issues.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/errors 的工作流错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:WorkflowHasIssuesError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/errors/workflow-has-issues.error.ts -> services/n8n/application/core/services/execution_engine/errors/workflow_has_issues_error.py

import { WorkflowOperationError } from 'n8n-workflow';

export class WorkflowHasIssuesError extends WorkflowOperationError {
	constructor() {
		super('The workflow has issues and cannot be executed for that reason. Please fix them first.');
	}
}
