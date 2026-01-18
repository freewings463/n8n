"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1621707690587-AddWaitColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddWaitColumn1621707690587。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1621707690587-AddWaitColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1621707690587_AddWaitColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddWaitColumn1621707690587 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE IF EXISTS "${tablePrefix}temporary_execution_entity"`);
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}temporary_execution_entity" ("id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "data" text NOT NULL, "finished" boolean NOT NULL, "mode" varchar NOT NULL, "retryOf" varchar, "retrySuccessId" varchar, "startedAt" datetime NOT NULL, "stoppedAt" datetime, "workflowData" text NOT NULL, "workflowId" varchar, "waitTill" DATETIME)`,
		);
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}temporary_execution_entity"("id", "data", "finished", "mode", "retryOf", "retrySuccessId", "startedAt", "stoppedAt", "workflowData", "workflowId") SELECT "id", "data", "finished", "mode", "retryOf", "retrySuccessId", "startedAt", "stoppedAt", "workflowData", "workflowId" FROM "${tablePrefix}execution_entity"`,
		);
		await queryRunner.query(`DROP TABLE "${tablePrefix}execution_entity"`);
		await queryRunner.query(
			`ALTER TABLE "${tablePrefix}temporary_execution_entity" RENAME TO "${tablePrefix}execution_entity"`,
		);
		await queryRunner.query(
			`CREATE INDEX "IDX_${tablePrefix}cefb067df2402f6aed0638a6c1" ON "${tablePrefix}execution_entity" ("stoppedAt")`,
		);
		await queryRunner.query(
			`CREATE INDEX "IDX_${tablePrefix}ca4a71b47f28ac6ea88293a8e2" ON "${tablePrefix}execution_entity" ("waitTill")`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE IF NOT EXISTS "${tablePrefix}temporary_execution_entity" ("id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, "data" text NOT NULL, "finished" boolean NOT NULL, "mode" varchar NOT NULL, "retryOf" varchar, "retrySuccessId" varchar, "startedAt" datetime NOT NULL, "stoppedAt" datetime, "workflowData" text NOT NULL, "workflowId" varchar)`,
		);
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}temporary_execution_entity"("id", "data", "finished", "mode", "retryOf", "retrySuccessId", "startedAt", "stoppedAt", "workflowData", "workflowId") SELECT "id", "data", "finished", "mode", "retryOf", "retrySuccessId", "startedAt", "stoppedAt", "workflowData", "workflowId" FROM "${tablePrefix}execution_entity"`,
		);
		await queryRunner.query(`DROP TABLE "${tablePrefix}execution_entity"`);
		await queryRunner.query(
			`ALTER TABLE "${tablePrefix}temporary_execution_entity" RENAME TO "${tablePrefix}execution_entity"`,
		);
		await queryRunner.query(
			`CREATE INDEX "IDX_${tablePrefix}cefb067df2402f6aed0638a6c1" ON "${tablePrefix}execution_entity" ("stoppedAt")`,
		);
	}
}
