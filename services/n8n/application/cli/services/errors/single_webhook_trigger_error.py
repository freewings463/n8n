"""
MIGRATION-META:
  source_path: packages/cli/src/errors/single-webhook-trigger.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SingleWebhookTriggerError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/single-webhook-trigger.error.ts -> services/n8n/application/cli/services/errors/single_webhook_trigger_error.py

import { UserError } from 'n8n-workflow';

export class SingleWebhookTriggerError extends UserError {
	constructor(triggerName: string) {
		super(
			`Because of limitations in ${triggerName}, n8n can't listen for test executions at the same time as listening for production ones. Unpublish the workflow to execute.`,
			{ extra: { triggerName } },
		);
	}
}
