"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1594902918301-CreateIndexStoppedAt.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateIndexStoppedAt1594902918301。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1594902918301-CreateIndexStoppedAt.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1594902918301_CreateIndexStoppedAt.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateIndexStoppedAt1594902918301 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			'CREATE INDEX `IDX_' +
				tablePrefix +
				'cefb067df2402f6aed0638a6c1` ON `' +
				tablePrefix +
				'execution_entity` (`stoppedAt`)',
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			'DROP INDEX `IDX_' +
				tablePrefix +
				'cefb067df2402f6aed0638a6c1` ON `' +
				tablePrefix +
				'execution_entity`',
		);
	}
}
