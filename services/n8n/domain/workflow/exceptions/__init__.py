"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/index.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:BaseError、type BaseErrorOptions、OperationalError、type OperationalErrorOptions、UnexpectedError、type UnexpectedErrorOptions、UserError、type UserErrorOptions 等19项。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/index.ts -> services/n8n/domain/workflow/exceptions/__init__.py

export { BaseError, type BaseErrorOptions } from './base/base.error';
export { OperationalError, type OperationalErrorOptions } from './base/operational.error';
export { UnexpectedError, type UnexpectedErrorOptions } from './base/unexpected.error';
export { UserError, type UserErrorOptions } from './base/user.error';
export { ApplicationError } from '@n8n/errors';
export { ExpressionError } from './expression.error';
export {
	ExecutionCancelledError,
	ManualExecutionCancelledError,
	SystemShutdownExecutionCancelledError,
	TimeoutExecutionCancelledError,
	type CancellationReason,
} from './execution-cancelled.error';
export { NodeApiError } from './node-api.error';
export { NodeOperationError } from './node-operation.error';
export { WorkflowConfigurationError } from './workflow-configuration.error';
export { NodeSslError } from './node-ssl.error';
export { WebhookPathTakenError } from './webhook-taken.error';
export { WorkflowActivationError } from './workflow-activation.error';
export { WorkflowDeactivationError } from './workflow-deactivation.error';
export { WorkflowOperationError } from './workflow-operation.error';
export { SubworkflowOperationError } from './subworkflow-operation.error';
export { CliWorkflowOperationError } from './cli-subworkflow-operation.error';
export { TriggerCloseError } from './trigger-close.error';

export { NodeError } from './abstract/node.error';
export { ExecutionBaseError } from './abstract/execution-base.error';
export { ExpressionExtensionError } from './expression-extension.error';
export { ExpressionDestructuringError } from './expression-destructuring.error';
export { DbConnectionTimeoutError } from './db-connection-timeout-error';
export { ensureError } from './ensure-error';
