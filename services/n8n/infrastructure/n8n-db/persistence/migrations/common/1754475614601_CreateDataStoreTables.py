"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1754475614601-CreateDataStoreTables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateDataStoreTables1754475614601。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1754475614601-CreateDataStoreTables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1754475614601_CreateDataStoreTables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const DATA_STORE_TABLE_NAME = 'data_store';
const DATA_STORE_COLUMN_TABLE_NAME = 'data_store_column';

export class CreateDataStoreTables1754475614601 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(DATA_STORE_TABLE_NAME)
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

		await createTable(DATA_STORE_COLUMN_TABLE_NAME)
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
				tableName: DATA_STORE_TABLE_NAME,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withUniqueConstraintOn(['dataStoreId', 'name']).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(DATA_STORE_COLUMN_TABLE_NAME);
		await dropTable(DATA_STORE_TABLE_NAME);
	}
}
