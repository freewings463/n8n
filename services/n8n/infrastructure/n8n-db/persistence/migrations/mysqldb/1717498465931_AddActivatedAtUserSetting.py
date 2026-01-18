"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1717498465931-AddActivatedAtUserSetting.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddActivatedAtUserSetting1717498465931。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1717498465931-AddActivatedAtUserSetting.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1717498465931_AddActivatedAtUserSetting.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddActivatedAtUserSetting1717498465931 implements ReversibleMigration {
	async up({ queryRunner, escape }: MigrationContext) {
		const now = Date.now();
		await queryRunner.query(
			`UPDATE ${escape.tableName('user')}
			SET settings = JSON_SET(COALESCE(settings, '{}'), '$.userActivatedAt', '${now}')
			WHERE settings IS NOT NULL AND JSON_EXTRACT(settings, '$.userActivated') = true`,
		);
	}

	async down({ queryRunner, escape }: MigrationContext) {
		await queryRunner.query(
			`UPDATE ${escape.tableName('user')}
			SET settings = JSON_REMOVE(settings, '$.userActivatedAt')
			WHERE settings IS NOT NULL`,
		);
	}
}
