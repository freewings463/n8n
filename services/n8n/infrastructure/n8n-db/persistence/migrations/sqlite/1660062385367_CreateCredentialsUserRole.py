"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1660062385367-CreateCredentialsUserRole.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateCredentialsUserRole1660062385367。关键函数/方法:up、VALUES、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1660062385367-CreateCredentialsUserRole.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1660062385367_CreateCredentialsUserRole.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateCredentialsUserRole1660062385367 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`
			INSERT INTO "${tablePrefix}role" (name, scope)
			VALUES ("user", "credential")
			ON CONFLICT DO NOTHING;
		`);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`
			DELETE FROM "${tablePrefix}role" WHERE name='user' AND scope='credential';
		`);
	}
}
