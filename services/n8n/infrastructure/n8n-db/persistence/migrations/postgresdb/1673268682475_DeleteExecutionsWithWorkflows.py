"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1673268682475-DeleteExecutionsWithWorkflows.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:DeleteExecutionsWithWorkflows1673268682475。关键函数/方法:up、workflowIds、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1673268682475-DeleteExecutionsWithWorkflows.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1673268682475_DeleteExecutionsWithWorkflows.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class DeleteExecutionsWithWorkflows1673268682475 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}execution_entity
			 ALTER COLUMN "workflowId" TYPE INTEGER USING "workflowId"::integer`,
		);

		const workflowIds = (await queryRunner.query(`
			SELECT id FROM ${tablePrefix}workflow_entity
		`)) as Array<{ id: number }>;

		await queryRunner.query(
			`DELETE FROM ${tablePrefix}execution_entity
			 WHERE "workflowId" IS NOT NULL
			 ${
					workflowIds.length
						? `AND "workflowId" NOT IN (${workflowIds.map(({ id }) => id).join()})`
						: ''
				}`,
		);

		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}execution_entity
			 ADD CONSTRAINT "FK_${tablePrefix}execution_entity_workflowId"
			 FOREIGN KEY ("workflowId") REFERENCES ${tablePrefix}workflow_entity ("id")
			 ON DELETE CASCADE`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}execution_entity
			 DROP CONSTRAINT "FK_${tablePrefix}execution_entity_workflowId"`,
		);

		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}execution_entity
			 ALTER COLUMN "workflowId" TYPE TEXT`,
		);
	}
}
