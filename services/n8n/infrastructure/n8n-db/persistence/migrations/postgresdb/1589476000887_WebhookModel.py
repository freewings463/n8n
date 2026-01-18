"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1589476000887-WebhookModel.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:WebhookModel1589476000887。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1589476000887-WebhookModel.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1589476000887_WebhookModel.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class WebhookModel1589476000887 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE IF NOT EXISTS ${tablePrefix}webhook_entity ("workflowId" integer NOT NULL, "webhookPath" character varying NOT NULL, "method" character varying NOT NULL, "node" character varying NOT NULL, CONSTRAINT "PK_${tablePrefix}b21ace2e13596ccd87dc9bf4ea6" PRIMARY KEY ("webhookPath", "method"))`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE ${tablePrefix}webhook_entity`);
	}
}
