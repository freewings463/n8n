"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1761047826451-AddWorkflowVersionColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddWorkflowVersionColumn1761047826451。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1761047826451-AddWorkflowVersionColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1761047826451_AddWorkflowVersionColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

/**
 * SQLite-specific migration to add versionCounter column and trigger for auto-incrementing.
 */
export class AddWorkflowVersionColumn1761047826451 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const tableName = `${tablePrefix}workflow_entity`;
		const triggerName = `${tablePrefix}workflow_version_increment`;

		// Add versionCounter column
		await queryRunner.query(
			`ALTER TABLE ${tableName} ADD COLUMN "versionCounter" integer NOT NULL DEFAULT 1`,
		);

		// Create trigger that increments version counter on update.
		// NOTE: we perform the version counter bump AFTER so it isn't overwritten by the original update.
		await queryRunner.query(`
			CREATE TRIGGER ${triggerName}
			AFTER UPDATE ON ${tableName}
			FOR EACH ROW
			WHEN OLD."versionCounter" = NEW."versionCounter"
			BEGIN
				UPDATE ${tableName}
				SET "versionCounter" = "versionCounter" + 1
				WHERE id = NEW.id;
			END;
		`);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		const tableName = `${tablePrefix}workflow_entity`;
		const triggerName = `${tablePrefix}workflow_version_increment`;

		// Drop trigger
		await queryRunner.query(`DROP TRIGGER IF EXISTS ${triggerName}`);

		// Drop column
		await queryRunner.query(`ALTER TABLE ${tableName} DROP COLUMN "versionCounter"`);
	}
}
