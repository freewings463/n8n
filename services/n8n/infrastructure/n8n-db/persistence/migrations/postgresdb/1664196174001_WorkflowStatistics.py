"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1664196174001-WorkflowStatistics.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:WorkflowStatistics1664196174001。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1664196174001-WorkflowStatistics.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1664196174001_WorkflowStatistics.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class WorkflowStatistics1664196174001 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		// Create statistics table
		await queryRunner.query(
			`CREATE TABLE ${tablePrefix}workflow_statistics (
				"count" INTEGER DEFAULT 0,
				"latestEvent" TIMESTAMP,
				"name" VARCHAR(128) NOT NULL,
				"workflowId" INTEGER,
				PRIMARY KEY("workflowId", "name"),
				FOREIGN KEY("workflowId") REFERENCES ${tablePrefix}workflow_entity("id") ON DELETE CASCADE
			)`,
		);

		// Add dataLoaded column to workflow table
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}workflow_entity ADD COLUMN "dataLoaded" BOOLEAN DEFAULT false;`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE ${tablePrefix}workflow_statistics`);
		await queryRunner.query(`ALTER TABLE ${tablePrefix}workflow_entity DROP COLUMN dataLoaded`);
	}
}
