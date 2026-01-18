"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1690000000031-FixExecutionDataType.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:FixExecutionDataType1690000000031。关键函数/方法:up。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1690000000031-FixExecutionDataType.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1690000000031_FixExecutionDataType.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class FixExecutionDataType1690000000031 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		/**
		 * SeparateExecutionData migration for MySQL/MariaDB accidentally changed the data-type for `data` column to `TEXT`.
		 * This migration changes it back.
		 * The previous migration has been patched to avoid converting to `TEXT`, which might fail.
		 *
		 * For any users who already ran the previous migration, this migration should fix the column type.
		 * For any users who run these migrations in the same batch, this migration would be no-op, as the column type is already `MEDIUMTEXT`
		 */
		await queryRunner.query(
			'ALTER TABLE `' + tablePrefix + 'execution_data` MODIFY COLUMN `data` MEDIUMTEXT',
		);
	}
}
