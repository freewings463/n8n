"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1588102412422-InitialMigration.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:InitialMigration1588102412422。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1588102412422-InitialMigration.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1588102412422_InitialMigration.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class InitialMigration1588102412422 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE IF NOT EXISTS "${tablePrefix}credentials_entity" ("id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "name" varchar(128) NOT NULL, "data" text NOT NULL, "type" varchar(128) NOT NULL, "nodesAccess" text NOT NULL, "createdAt" datetime NOT NULL, "updatedAt" datetime NOT NULL)`,
		);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS "IDX_${tablePrefix}07fde106c0b471d8cc80a64fc8" ON "${tablePrefix}credentials_entity" ("type") `,
		);
		await queryRunner.query(
			`CREATE TABLE IF NOT EXISTS "${tablePrefix}execution_entity" ("id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "data" text NOT NULL, "finished" boolean NOT NULL, "mode" varchar NOT NULL, "retryOf" varchar, "retrySuccessId" varchar, "startedAt" datetime NOT NULL, "stoppedAt" datetime NOT NULL, "workflowData" text NOT NULL, "workflowId" varchar)`,
		);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS "IDX_${tablePrefix}c4d999a5e90784e8caccf5589d" ON "${tablePrefix}execution_entity" ("workflowId") `,
		);
		await queryRunner.query(
			`CREATE TABLE IF NOT EXISTS "${tablePrefix}workflow_entity" ("id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "name" varchar(128) NOT NULL, "active" boolean NOT NULL, "nodes" text NOT NULL, "connections" text NOT NULL, "createdAt" datetime NOT NULL, "updatedAt" datetime NOT NULL, "settings" text, "staticData" text)`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}workflow_entity"`);
		await queryRunner.query(`DROP INDEX "IDX_${tablePrefix}c4d999a5e90784e8caccf5589d"`);
		await queryRunner.query(`DROP TABLE "${tablePrefix}execution_entity"`);
		await queryRunner.query(`DROP INDEX "IDX_${tablePrefix}07fde106c0b471d8cc80a64fc8"`);
		await queryRunner.query(`DROP TABLE "${tablePrefix}credentials_entity"`);
	}
}
