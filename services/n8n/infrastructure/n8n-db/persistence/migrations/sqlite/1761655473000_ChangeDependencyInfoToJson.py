"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1761655473000-ChangeDependencyInfoToJson.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ChangeDependencyInfoToJson1761655473000。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1761655473000-ChangeDependencyInfoToJson.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1761655473000_ChangeDependencyInfoToJson.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

/**
 * SQLite-specific migration to change the `dependencyInfo` column in `workflow_dependency` table from VARCHAR(255) to JSON.
 * SQLite doesn't support ALTER COLUMN, so we drop and recreate the column.
 * Since the table is empty at this point, this is safe.
 */
export class ChangeDependencyInfoToJson1761655473000 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const tableName = `${tablePrefix}workflow_dependency`;

		// SQLite doesn't support ALTER COLUMN, so drop and recreate the column
		await queryRunner.query(`ALTER TABLE "${tableName}" DROP COLUMN "dependencyInfo"`);
		await queryRunner.query(
			`ALTER TABLE "${tableName}" ADD COLUMN "dependencyInfo" TEXT CONSTRAINT workflow_dependency_chk_dependency_info_is_json CHECK("dependencyInfo" IS NULL OR json_valid("dependencyInfo"))`,
		);
	}
}
