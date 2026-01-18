"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/workflow-configuration.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:无；本地:./node-operation.error。导出:WorkflowConfigurationError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/workflow-configuration.error.ts -> services/n8n/domain/workflow/exceptions/workflow_configuration_error.py

import { NodeOperationError } from './node-operation.error';

/**
 * A type of NodeOperationError caused by a configuration problem somewhere in workflow.
 */
export class WorkflowConfigurationError extends NodeOperationError {}
