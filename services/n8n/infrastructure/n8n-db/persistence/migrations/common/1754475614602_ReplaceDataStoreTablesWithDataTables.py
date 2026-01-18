"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1754475614602-ReplaceDataStoreTablesWithDataTables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ReplaceDataStoreTablesWithDataTables1754475614602。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1754475614602-ReplaceDataStoreTablesWithDataTables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1754475614602_ReplaceDataStoreTablesWithDataTables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const TABLE_TABLE_NAME_BEFORE = 'data_store';
const COLUMN_TABLE_NAME_BEFORE = 'data_store_column';

const TABLE_TABLE_NAME_AFTER = 'data_table';
const COLUMN_TABLE_NAME_AFTER = 'data_table_column';

export class ReplaceDataStoreTablesWithDataTables1754475614602 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column, dropTable } }: MigrationContext) {
		await dropTable(COLUMN_TABLE_NAME_BEFORE);
		await dropTable(TABLE_TABLE_NAME_BEFORE);

		await createTable(TABLE_TABLE_NAME_AFTER)
			.withColumns(
				column('id').varchar(36).primary,
				column('name').varchar(128).notNull,
				column('projectId').varchar(36).notNull,
			)
			.withForeignKey('projectId', {
				tableName: 'project',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withUniqueConstraintOn(['projectId', 'name']).withTimestamps;

		await createTable(COLUMN_TABLE_NAME_AFTER)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('name').varchar(128).notNull,
				column('type')
					.varchar(32)
					.notNull.comment(
						'Expected: string, number, boolean, or date (not enforced as a constraint)',
					),
				column('index').int.notNull.comment('Column order, starting from 0 (0 = first column)'),
				column('dataTableId').varchar(36).notNull,
			)
			.withForeignKey('dataTableId', {
				tableName: TABLE_TABLE_NAME_AFTER,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withUniqueConstraintOn(['dataTableId', 'name']).withTimestamps;
	}

	async down({ schemaBuilder: { createTable, column, dropTable } }: MigrationContext) {
		await dropTable(COLUMN_TABLE_NAME_AFTER);
		await dropTable(TABLE_TABLE_NAME_AFTER);

		await createTable(TABLE_TABLE_NAME_BEFORE)
			.withColumns(
				column('id').varchar(36).primary,
				column('name').varchar(128).notNull,
				column('projectId').varchar(36).notNull,
				column('sizeBytes').int.default(0).notNull,
			)
			.withForeignKey('projectId', {
				tableName: 'project',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withUniqueConstraintOn(['projectId', 'name']).withTimestamps;

		await createTable(COLUMN_TABLE_NAME_BEFORE)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('name').varchar(128).notNull,
				column('type')
					.varchar(32)
					.notNull.comment(
						'Expected: string, number, boolean, or date (not enforced as a constraint)',
					),
				column('index').int.notNull.comment('Column order, starting from 0 (0 = first column)'),
				column('dataStoreId').varchar(36).notNull,
			)
			.withForeignKey('dataStoreId', {
				tableName: TABLE_TABLE_NAME_BEFORE,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withUniqueConstraintOn(['dataStoreId', 'name']).withTimestamps;
	}
}
