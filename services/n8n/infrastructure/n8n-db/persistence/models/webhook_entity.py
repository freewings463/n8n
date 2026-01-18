"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/webhook-entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的Webhook模块。导入/依赖:外部:无；内部:@n8n/typeorm、n8n-workflow；本地:无。导出:WebhookEntity。关键函数/方法:display。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/webhook-entity.ts -> services/n8n/infrastructure/n8n-db/persistence/models/webhook_entity.py

import { Column, Entity, Index, PrimaryColumn } from '@n8n/typeorm';
import { IHttpRequestMethods } from 'n8n-workflow';

@Entity()
@Index(['webhookId', 'method', 'pathLength'])
export class WebhookEntity {
	@Column()
	workflowId: string;

	@PrimaryColumn()
	webhookPath: string;

	@PrimaryColumn({ type: 'text' })
	method: IHttpRequestMethods;

	@Column()
	node: string;

	@Column({ nullable: true })
	webhookId?: string;

	@Column({ nullable: true })
	pathLength?: number;

	/**
	 * Unique section of webhook path.
	 *
	 * - Static: `${uuid}` or `user/defined/path`
	 * - Dynamic: `${uuid}/user/:id/posts`
	 *
	 * Appended to `${instanceUrl}/webhook/` or `${instanceUrl}/test-webhook/`.
	 */
	private get uniquePath() {
		return this.webhookPath.includes(':')
			? [this.webhookId, this.webhookPath].join('/')
			: this.webhookPath;
	}

	get cacheKey() {
		return `webhook:${this.method}-${this.uniquePath}`;
	}

	get staticSegments() {
		return this.webhookPath.split('/').filter((s) => !s.startsWith(':'));
	}

	/**
	 * Whether the webhook has at least one dynamic path segment, e.g. `:id` in `<uuid>/user/:id/posts`.
	 */
	get isDynamic() {
		return this.webhookPath.split('/').some((s) => s.startsWith(':'));
	}

	display() {
		return `${this.method} ${this.webhookPath}`;
	}
}
