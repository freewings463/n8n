"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1607431743769-MakeStoppedAtNullable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MakeStoppedAtNullable1607431743769。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1607431743769-MakeStoppedAtNullable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1607431743769_MakeStoppedAtNullable.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class MakeStoppedAtNullable1607431743769 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		// SQLite does not allow us to simply "alter column"
		// We're hacking the way sqlite identifies tables
		// Allowing a column to become nullable
		// This is a very strict case when this can be done safely
		// As no collateral effects exist.
		await queryRunner.query('PRAGMA writable_schema = 1;');
		await queryRunner.query(
			`UPDATE SQLITE_MASTER SET SQL = 'CREATE TABLE IF NOT EXISTS "${tablePrefix}execution_entity" ("id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "data" text NOT NULL, "finished" boolean NOT NULL, "mode" varchar NOT NULL, "retryOf" varchar, "retrySuccessId" varchar, "startedAt" datetime NOT NULL, "stoppedAt" datetime, "workflowData" text NOT NULL, "workflowId" varchar)' WHERE NAME = "${tablePrefix}execution_entity";`,
		);
		await queryRunner.query('PRAGMA writable_schema = 0;');
	}
}
