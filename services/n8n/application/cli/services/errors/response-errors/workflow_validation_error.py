"""
MIGRATION-META:
  source_path: packages/cli/src/errors/response-errors/workflow-validation.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors/response-errors 的工作流错误。导入/依赖:外部:无；内部:无；本地:./bad-request.error。导出:WorkflowValidationError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/response-errors/workflow-validation.error.ts -> services/n8n/application/cli/services/errors/response-errors/workflow_validation_error.py

import { BadRequestError } from './bad-request.error';

/**
 * Error thrown when a workflow fails validation before activation.
 */
export class WorkflowValidationError extends BadRequestError {
	readonly meta = { validationError: true as const };

	constructor(message: string) {
		super(message);
		this.name = 'WorkflowValidationError';
	}
}
