"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1732271325258-CreateTestMetricTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:node:assert；内部:无；本地:../migration-types。导出:CreateTestMetricTable1732271325258。关键函数/方法:up、assert、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1732271325258-CreateTestMetricTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1732271325258_CreateTestMetricTable.py

import assert from 'node:assert';

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const testMetricEntityTableName = 'test_metric';

export class CreateTestMetricTable1732271325258 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column }, queryRunner, tablePrefix }: MigrationContext) {
		// Check if the previous migration MigrateTestDefinitionKeyToString1731582748663 properly updated the primary key
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
		// End of test_definition PK check

		await createTable(testMetricEntityTableName)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('name').varchar(255).notNull,
				column('testDefinitionId').varchar(36).notNull,
			)
			.withIndexOn('testDefinitionId')
			.withForeignKey('testDefinitionId', {
				tableName: 'test_definition',
				columnName: 'id',
				onDelete: 'CASCADE',
			}).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(testMetricEntityTableName);
	}
}
