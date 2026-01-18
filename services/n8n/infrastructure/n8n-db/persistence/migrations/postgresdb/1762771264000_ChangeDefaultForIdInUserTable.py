"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1762771264000-ChangeDefaultForIdInUserTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ChangeDefaultForIdInUserTable1762771264000。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1762771264000-ChangeDefaultForIdInUserTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1762771264000_ChangeDefaultForIdInUserTable.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

/**
 * PostgreSQL-specific migration to change the default value for the `id` column in `user` table.
 * The previous default implementation was based on MD5 hashing to produce a random UUID, but
 * MD5 is not supported in FIPS compliant postgres environments. We are switching to `gen_random_uuid()`
 * which is supported in versions of PostgreSQL since 13.
 */
export class ChangeDefaultForIdInUserTable1762771264000 implements IrreversibleMigration {
	async up({ queryRunner, escape }: MigrationContext) {
		const tableName = escape.tableName('user');
		const idColumnName = escape.columnName('id');

		await queryRunner.query(
			`ALTER TABLE ${tableName} ALTER COLUMN ${idColumnName} SET DEFAULT gen_random_uuid()`,
		);
	}
}
