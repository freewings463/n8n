"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1673268682475-DeleteExecutionsWithWorkflows.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:DeleteExecutionsWithWorkflows1673268682475。关键函数/方法:up、workflowIds、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1673268682475-DeleteExecutionsWithWorkflows.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1673268682475_DeleteExecutionsWithWorkflows.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class DeleteExecutionsWithWorkflows1673268682475 implements ReversibleMigration {
	transaction = false as const;

	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const workflowIds = (await queryRunner.query(`
			SELECT id FROM "${tablePrefix}workflow_entity"
		`)) as Array<{ id: number }>;

		await queryRunner.query(
			`DELETE FROM "${tablePrefix}execution_entity"
			 WHERE "workflowId" IS NOT NULL
			 ${
					workflowIds.length
						? `AND "workflowId" NOT IN (${workflowIds.map(({ id }) => id).join()})`
						: ''
				}`,
		);

		await queryRunner.query(`DROP TABLE IF EXISTS "${tablePrefix}temporary_execution_entity"`);
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}temporary_execution_entity" (
				"id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
				"workflowId" int,
				"finished" boolean NOT NULL,
				"mode" varchar NOT NULL,
				"retryOf" varchar,
				"retrySuccessId" varchar,
				"startedAt" datetime NOT NULL,
				"stoppedAt" datetime,
				"waitTill" datetime,
				"workflowData" text NOT NULL,
				"data" text NOT NULL,
				FOREIGN KEY("workflowId") REFERENCES "${tablePrefix}workflow_entity" ("id") ON DELETE CASCADE
			)`,
		);

		const columns =
			'"id", "workflowId", "finished", "mode", "retryOf", "retrySuccessId", "startedAt", "stoppedAt", "waitTill", "workflowData", "data"';
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}temporary_execution_entity"(${columns}) SELECT ${columns} FROM "${tablePrefix}execution_entity"`,
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
		await queryRunner.query(`DROP TABLE IF EXISTS "${tablePrefix}temporary_execution_entity"`);
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}temporary_execution_entity" (
				"id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
				"workflowId" varchar,
				"finished" boolean NOT NULL,
				"mode" varchar NOT NULL,
				"retryOf" varchar,
				"retrySuccessId" varchar,
				"startedAt" datetime NOT NULL,
				"stoppedAt" datetime,
				"waitTill" datetime,
				"workflowData" text NOT NULL,
				"data" text NOT NULL
			)`,
		);

		const columns =
			'"id", "workflowId", "finished", "mode", "retryOf", "retrySuccessId", "startedAt", "stoppedAt", "waitTill", "workflowData", "data"';
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}temporary_execution_entity"(${columns}) SELECT ${columns} FROM "${tablePrefix}execution_entity"`,
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
}
