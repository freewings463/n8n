"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhooks.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook控制器。导入/依赖:外部:express、lodash/get；内部:@n8n/decorators；本地:./webhook.service、./webhook.types。导出:WebhooksController。关键函数/方法:findWebhook。用于处理Webhook接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhooks.controller.ts -> services/n8n/presentation/cli/api/webhooks/webhooks_controller.py

import { Post, RestController } from '@n8n/decorators';
import { Request } from 'express';
import get from 'lodash/get';

import { WebhookService } from './webhook.service';
import type { Method } from './webhook.types';

@RestController('/webhooks')
export class WebhooksController {
	constructor(private readonly webhookService: WebhookService) {}

	@Post('/find')
	async findWebhook(req: Request) {
		const body = get(req, 'body', {}) as { path: string; method: Method };

		try {
			const webhook = await this.webhookService.findWebhook(body.method, body.path);
			return webhook;
		} catch (error) {
			return null;
		}
	}
}
