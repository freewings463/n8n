"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhook-on-received-response-extractor.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:extractWebhookOnReceivedResponse。关键函数/方法:extractWebhookOnReceivedResponse。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Webhook HTTP entry -> presentation/api/v1/controllers/webhooks
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhook-on-received-response-extractor.ts -> services/n8n/presentation/cli/api/v1/controllers/webhooks/webhook_on_received_response_extractor.py

import type { IWebhookResponseData, WebhookResponseData } from 'n8n-workflow';

/**
+ * Creates the response for a webhook when the response mode is set to
 * `onReceived`.
 *
 * @param context - The webhook execution context
 * @param responseData - The evaluated `responseData` option of the webhook node
 * @param webhookResultData - The webhook result data that the webhook might have returned when it was ran
 *
 * @returns The response body
 */
export function extractWebhookOnReceivedResponse(
	// eslint-disable-next-line @typescript-eslint/no-redundant-type-constituents
	responseData: Extract<WebhookResponseData, 'noData'> | string | undefined,
	webhookResultData: IWebhookResponseData,
): unknown {
	// Return response directly and do not wait for the workflow to finish
	if (responseData === 'noData') {
		return undefined;
	}

	if (responseData) {
		return responseData;
	}

	if (webhookResultData.webhookResponse !== undefined) {
		// Data to respond with is given
		return webhookResultData.webhookResponse as unknown;
	}

	return { message: 'Workflow was started' };
}
