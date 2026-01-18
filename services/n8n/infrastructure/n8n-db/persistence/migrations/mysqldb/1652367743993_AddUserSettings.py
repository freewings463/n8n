"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1652367743993-AddUserSettings.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddUserSettings1652367743993。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1652367743993-AddUserSettings.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1652367743993_AddUserSettings.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddUserSettings1652367743993 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			'ALTER TABLE `' + tablePrefix + 'user` ADD COLUMN `settings` json NULL DEFAULT NULL',
		);
		await queryRunner.query(
			'ALTER TABLE `' +
				tablePrefix +
				'user` CHANGE COLUMN `personalizationAnswers` `personalizationAnswers` json NULL DEFAULT NULL',
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query('ALTER TABLE `' + tablePrefix + 'user` DROP COLUMN `settings`');
	}
}
