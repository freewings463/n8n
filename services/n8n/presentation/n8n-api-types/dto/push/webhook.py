"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/push/webhook.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/push 的Webhook模块。导入/依赖:外部:无；内部:无；本地:无。导出:TestWebhookDeleted、TestWebhookReceived、WebhookPushMessage。关键函数/方法:无。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/push/webhook.ts -> services/n8n/presentation/n8n-api-types/dto/push/webhook.py

export type TestWebhookDeleted = {
	type: 'testWebhookDeleted';
	data: {
		executionId?: string;
		workflowId: string;
	};
};

export type TestWebhookReceived = {
	type: 'testWebhookReceived';
	data: {
		executionId: string;
		workflowId: string;
	};
};

export type WebhookPushMessage = TestWebhookDeleted | TestWebhookReceived;
