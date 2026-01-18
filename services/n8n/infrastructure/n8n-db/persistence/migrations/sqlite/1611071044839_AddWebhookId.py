"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1611071044839-AddWebhookId.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddWebhookId1611071044839。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1611071044839-AddWebhookId.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1611071044839_AddWebhookId.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddWebhookId1611071044839 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			'CREATE TABLE "temporary_webhook_entity" ("workflowId" integer NOT NULL, "webhookPath" varchar NOT NULL, "method" varchar NOT NULL, "node" varchar NOT NULL, "webhookId" varchar, "pathLength" integer, PRIMARY KEY ("webhookPath", "method"))',
		);
		await queryRunner.query(
			`INSERT INTO "temporary_webhook_entity"("workflowId", "webhookPath", "method", "node") SELECT "workflowId", "webhookPath", "method", "node" FROM "${tablePrefix}webhook_entity"`,
		);
		await queryRunner.query(`DROP TABLE "${tablePrefix}webhook_entity"`);
		await queryRunner.query(
			`ALTER TABLE "temporary_webhook_entity" RENAME TO "${tablePrefix}webhook_entity"`,
		);
		await queryRunner.query(
			`CREATE INDEX "IDX_${tablePrefix}742496f199721a057051acf4c2" ON "${tablePrefix}webhook_entity" ("webhookId", "method", "pathLength") `,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP INDEX "IDX_${tablePrefix}742496f199721a057051acf4c2"`);
		await queryRunner.query(
			`ALTER TABLE "${tablePrefix}webhook_entity" RENAME TO "temporary_webhook_entity"`,
		);
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}webhook_entity" ("workflowId" integer NOT NULL, "webhookPath" varchar NOT NULL, "method" varchar NOT NULL, "node" varchar NOT NULL, PRIMARY KEY ("webhookPath", "method"))`,
		);
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}webhook_entity"("workflowId", "webhookPath", "method", "node") SELECT "workflowId", "webhookPath", "method", "node" FROM "temporary_webhook_entity"`,
		);
		await queryRunner.query('DROP TABLE "temporary_webhook_entity"');
	}
}
