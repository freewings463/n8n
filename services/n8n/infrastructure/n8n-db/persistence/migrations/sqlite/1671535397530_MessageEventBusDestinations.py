"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1671535397530-MessageEventBusDestinations.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MessageEventBusDestinations1671535397530。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1671535397530-MessageEventBusDestinations.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1671535397530_MessageEventBusDestinations.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class MessageEventBusDestinations1671535397530 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}event_destinations" (` +
				'"id"	varchar(36) PRIMARY KEY NOT NULL,' +
				'"destination" text NOT NULL,' +
				"\"createdAt\"	datetime(3) NOT NULL DEFAULT 'STRFTIME(''%Y-%m-%d %H:%M:%f'', ''NOW'')'," +
				"\"updatedAt\"	datetime(3) NOT NULL DEFAULT 'STRFTIME(''%Y-%m-%d %H:%M:%f'', ''NOW'')'" +
				');',
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}event_destinations"`);
	}
}
