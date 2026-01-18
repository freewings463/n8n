"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhook-server.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:无；内部:@n8n/di、@/abstract-server；本地:无。导出:WebhookServer。关键函数/方法:无。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhook-server.ts -> services/n8n/application/cli/services/webhooks/webhook_server.py

import { Service } from '@n8n/di';

import { AbstractServer } from '@/abstract-server';

@Service()
export class WebhookServer extends AbstractServer {}
