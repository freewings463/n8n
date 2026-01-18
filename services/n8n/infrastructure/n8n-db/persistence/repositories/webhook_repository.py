"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/webhook.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的Webhook仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:../entities。导出:WebhookRepository。关键函数/方法:getStaticWebhooks。用于封装Webhook数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/webhook.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/webhook_repository.py

import { Service } from '@n8n/di';
import { DataSource, IsNull, Repository } from '@n8n/typeorm';

import { WebhookEntity } from '../entities';

@Service()
export class WebhookRepository extends Repository<WebhookEntity> {
	constructor(dataSource: DataSource) {
		super(WebhookEntity, dataSource.manager);
	}

	/**
	 * Retrieve all webhooks whose paths only have static segments, e.g. `{uuid}` or `user/profile`.
	 * This excludes webhooks having paths with dynamic segments, e.g. `{uuid}/user/:id/posts`.
	 */
	async getStaticWebhooks() {
		return await this.findBy({ webhookId: IsNull() });
	}
}
