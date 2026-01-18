"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/webhook-helper-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的Webhook工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getWebhookDescription、getNodeWebhookUrl。关键函数/方法:getWebhookDescription、getNodeWebhookUrl。用于提供Webhook通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/webhook-helper-functions.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/webhook_helper_functions.py

import type {
	WebhookType,
	Workflow,
	INode,
	IWorkflowExecuteAdditionalData,
	WorkflowExecuteMode,
	IWorkflowDataProxyAdditionalKeys,
	IWebhookDescription,
} from 'n8n-workflow';
import { NodeHelpers } from 'n8n-workflow';

/** Returns the full webhook description of the webhook with the given name */
export function getWebhookDescription(
	name: WebhookType,
	workflow: Workflow,
	node: INode,
): IWebhookDescription | undefined {
	const nodeType = workflow.nodeTypes.getByNameAndVersion(node.type, node.typeVersion);

	// Node does not have any webhooks so return
	if (nodeType.description.webhooks === undefined) return;

	for (const webhookDescription of nodeType.description.webhooks) {
		if (webhookDescription.name === name) {
			return webhookDescription;
		}
	}

	return undefined;
}

/** Returns the webhook URL of the webhook with the given name */
export function getNodeWebhookUrl(
	name: WebhookType,
	workflow: Workflow,
	node: INode,
	additionalData: IWorkflowExecuteAdditionalData,
	mode: WorkflowExecuteMode,
	additionalKeys: IWorkflowDataProxyAdditionalKeys,
	isTest?: boolean,
): string | undefined {
	let baseUrl = additionalData.webhookBaseUrl;
	if (isTest === true) {
		baseUrl = additionalData.webhookTestBaseUrl;
	}

	const webhookDescription = getWebhookDescription(name, workflow, node);
	if (webhookDescription === undefined) return;

	const path = workflow.expression.getSimpleParameterValue(
		node,
		webhookDescription.path,
		mode,
		additionalKeys,
	);
	if (path === undefined) return;

	const isFullPath: boolean = workflow.expression.getSimpleParameterValue(
		node,
		webhookDescription.isFullPath,
		mode,
		additionalKeys,
		undefined,
		false,
	) as boolean;
	return NodeHelpers.getNodeWebhookUrl(baseUrl, workflow.id, node, path.toString(), isFullPath);
}
