"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1654089251344-IntroducePinData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:IntroducePinData1654089251344。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1654089251344-IntroducePinData.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1654089251344_IntroducePinData.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class IntroducePinData1654089251344 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}workflow_entity\` ADD COLUMN "pinData" text`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}workflow_entity\` RENAME TO "temporary_workflow_entity"`,
		);
		await queryRunner.query(
			`CREATE TABLE \`${tablePrefix}workflow_entity\` (
				"id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "name" varchar(128) NOT NULL, "active" boolean NOT NULL, "nodes" text NOT NULL, "connections" text NOT NULL, "createdAt" datetime NOT NULL, "updatedAt" datetime NOT NULL, "settings" text, "staticData" text`,
		);
		await queryRunner.query(
			`INSERT INTO \`${tablePrefix}workflow_entity\` ("id", "name", "active", "nodes", "connections", "createdAt", "updatedAt", "settings", "staticData") SELECT "id", "name", "active", "nodes", "connections", "createdAt", "updatedAt", "settings", "staticData" FROM "temporary_workflow_entity"`,
		);
		await queryRunner.query('DROP TABLE "temporary_workflow_entity"');
	}
}
