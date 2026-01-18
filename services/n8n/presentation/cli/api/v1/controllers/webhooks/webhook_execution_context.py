"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhook-execution-context.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:无；内部:无；本地:无。导出:WebhookExecutionContext。关键函数/方法:无。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Webhook HTTP entry -> presentation/api/v1/controllers/webhooks
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhook-execution-context.ts -> services/n8n/presentation/cli/api/v1/controllers/webhooks/webhook_execution_context.py

import type {
	IWebhookData,
	INode,
	IWorkflowDataProxyAdditionalKeys,
	Workflow,
	WorkflowExecuteMode,
	IExecuteData,
	IWebhookDescription,
	NodeParameterValueType,
} from 'n8n-workflow';

/**
 * A helper class that holds the context for the webhook execution.
 * Provides quality of life methods for evaluating expressions.
 */
export class WebhookExecutionContext {
	constructor(
		readonly workflow: Workflow,
		readonly workflowStartNode: INode,
		readonly webhookData: IWebhookData,
		readonly executionMode: WorkflowExecuteMode,
		readonly additionalKeys: IWorkflowDataProxyAdditionalKeys,
	) {}

	/**
	 * Evaluates a simple expression from the webhook description.
	 */
	evaluateSimpleWebhookDescriptionExpression<T extends boolean | number | string | unknown[]>(
		propertyName: keyof IWebhookDescription,
		executeData?: IExecuteData,
		defaultValue?: T,
	): T | undefined {
		return this.workflow.expression.getSimpleParameterValue(
			this.workflowStartNode,
			this.webhookData.webhookDescription[propertyName],
			this.executionMode,
			this.additionalKeys,
			executeData,
			defaultValue,
		) as T | undefined;
	}

	/**
	 * Evaluates a complex expression from the webhook description.
	 */
	evaluateComplexWebhookDescriptionExpression<T extends NodeParameterValueType>(
		propertyName: keyof IWebhookDescription,
		executeData?: IExecuteData,
		defaultValue?: T,
	): T | undefined {
		return this.workflow.expression.getComplexParameterValue(
			this.workflowStartNode,
			this.webhookData.webhookDescription[propertyName],
			this.executionMode,
			this.additionalKeys,
			executeData,
			defaultValue,
		) as T | undefined;
	}
}
