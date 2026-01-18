"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1626176912946-AddwaitTill.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddwaitTill1626176912946。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1626176912946-AddwaitTill.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1626176912946_AddwaitTill.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddwaitTill1626176912946 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`ALTER TABLE ${tablePrefix}execution_entity ADD "waitTill" TIMESTAMP`);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS IDX_${tablePrefix}ca4a71b47f28ac6ea88293a8e2 ON ${tablePrefix}execution_entity ("waitTill")`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP INDEX IDX_${tablePrefix}ca4a71b47f28ac6ea88293a8e2`);
		await queryRunner.query(`ALTER TABLE ${tablePrefix}webhook_entity DROP COLUMN "waitTill"`);
	}
}
