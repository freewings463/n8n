"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1739873751194-FixTestDefinitionPrimaryKey.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:node:assert；内部:无；本地:../migration-types。导出:FixTestDefinitionPrimaryKey1739873751194。关键函数/方法:up、assert。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1739873751194-FixTestDefinitionPrimaryKey.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1739873751194_FixTestDefinitionPrimaryKey.py

import assert from 'node:assert';

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class FixTestDefinitionPrimaryKey1739873751194 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		/**
		 * MigrateTestDefinitionKeyToString migration for MySQL/MariaDB had missing part,
		 * and didn't complete primary key type change and deletion of the temporary column.
		 *
		 * This migration checks if table is in inconsistent state and finishes the primary key type change when needed.
		 *
		 * The MigrateTestDefinitionKeyToString migration has been patched to properly change the primary key.
		 *
		 * As the primary key issue might prevent the CreateTestMetricTable migration from running successfully on MySQL 8.4.4,
		 * the CreateTestMetricTable also contains the patch.
		 *
		 * For users who already ran the MigrateTestDefinitionKeyToString and CreateTestMetricTable, this migration should fix the primary key.
		 * For users who run these migrations in the same batch, this migration would be no-op, as the test_definition table should be already fixed
		 * by either of the previous patched migrations.
		 */

		const table = await queryRunner.getTable(`${tablePrefix}test_definition`);
		assert(table, 'test_definition table not found');

		const brokenPrimaryColumn = table.primaryColumns.some(
			(c) => c.name === 'tmp_id' && c.isPrimary,
		);

		if (brokenPrimaryColumn) {
			// The migration was completed, but left the table in inconsistent state, let's finish the primary key change
			await queryRunner.query(
				`ALTER TABLE ${tablePrefix}test_definition MODIFY COLUMN tmp_id INT NOT NULL;`,
			);
			await queryRunner.query(
				`ALTER TABLE ${tablePrefix}test_definition DROP PRIMARY KEY, ADD PRIMARY KEY (\`id\`);`,
			);
			await queryRunner.query(
				`DROP INDEX \`TMP_idx_${tablePrefix}test_definition_id\` ON ${tablePrefix}test_definition;`,
			);
			await queryRunner.query(`ALTER TABLE ${tablePrefix}test_definition DROP COLUMN tmp_id;`);
		}
	}
}
