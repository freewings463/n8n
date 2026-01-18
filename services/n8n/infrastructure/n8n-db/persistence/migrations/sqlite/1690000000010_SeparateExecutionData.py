"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1690000000010-SeparateExecutionData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:SeparateExecutionData1690000000010。关键函数/方法:up、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1690000000010-SeparateExecutionData.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1690000000010_SeparateExecutionData.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class SeparateExecutionData1690000000010 implements ReversibleMigration {
	async up(context: MigrationContext): Promise<void> {
		const { queryRunner, tablePrefix } = context;

		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}execution_data" (
				"executionId" int PRIMARY KEY NOT NULL,
				"workflowData" text NOT NULL,
				"data" text NOT NULL,
				FOREIGN KEY("executionId") REFERENCES "${tablePrefix}execution_entity" ("id") ON DELETE CASCADE
			)`,
		);

		await context.copyTable(
			'execution_entity',
			'execution_data',
			['id', 'workflowData', 'data'],
			['executionId', 'workflowData', 'data'],
		);

		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}execution_entity\` DROP COLUMN "workflowData"`,
		);
		await queryRunner.query(`ALTER TABLE \`${tablePrefix}execution_entity\` DROP COLUMN "data"`);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext): Promise<void> {
		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}execution_entity\` ADD COLUMN "workflowData" text NULL`,
		);
		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}execution_entity\` ADD COLUMN "data" text NULL`,
		);

		await queryRunner.query(
			`UPDATE "${tablePrefix}execution_entity" SET "workflowData" = (SELECT "workflowData" FROM "${tablePrefix}execution_data" WHERE "${tablePrefix}execution_data"."executionId" = "${tablePrefix}execution_entity"."id")`,
		);
		await queryRunner.query(
			`UPDATE "${tablePrefix}execution_entity" SET "data" = (SELECT "data" FROM "${tablePrefix}execution_data" WHERE "${tablePrefix}execution_data"."executionId" = "${tablePrefix}execution_entity"."id")`,
		);

		await queryRunner.query(`DROP TABLE "${tablePrefix}execution_data"`);
	}
}
