"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1761047826451-AddWorkflowVersionColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddWorkflowVersionColumn1761047826451。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1761047826451-AddWorkflowVersionColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1761047826451_AddWorkflowVersionColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

/**
 * PostgreSQL-specific migration to add versionCounter column and trigger for auto-incrementing.
 */
export class AddWorkflowVersionColumn1761047826451 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const tableName = `${tablePrefix}workflow_entity`;
		const triggerName = `${tablePrefix}workflow_version_increment`;
		const functionName = `${tablePrefix}increment_workflow_version`;

		// Add versionCounter column
		await queryRunner.query(
			`ALTER TABLE ${tableName} ADD COLUMN "versionCounter" integer NOT NULL DEFAULT 1`,
		);

		// Create function that increments version counter.
		// NOTE: we're modifying the NEW record before the update happens, so we do it BEFORE the update.
		await queryRunner.query(`
			CREATE OR REPLACE FUNCTION ${functionName}()
			RETURNS TRIGGER AS $$
			BEGIN
				IF NEW."versionCounter" IS NOT DISTINCT FROM OLD."versionCounter" THEN
					NEW."versionCounter" = OLD."versionCounter" + 1;
				END IF;
				RETURN NEW;
			END;
			$$ LANGUAGE plpgsql;
		`);

		// Create trigger that calls the function before update
		await queryRunner.query(`
			CREATE TRIGGER ${triggerName}
			BEFORE UPDATE ON ${tableName}
			FOR EACH ROW
			EXECUTE FUNCTION ${functionName}();
		`);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		const tableName = `${tablePrefix}workflow_entity`;
		const triggerName = `${tablePrefix}workflow_version_increment`;
		const functionName = `${tablePrefix}increment_workflow_version`;

		// Drop trigger and function
		await queryRunner.query(`DROP TRIGGER IF EXISTS ${triggerName} ON ${tableName}`);
		await queryRunner.query(`DROP FUNCTION IF EXISTS ${functionName}`);

		// Drop column
		await queryRunner.query(`ALTER TABLE ${tableName} DROP COLUMN "versionCounter"`);
	}
}
