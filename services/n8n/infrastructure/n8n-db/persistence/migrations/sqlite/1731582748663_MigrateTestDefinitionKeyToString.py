"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1731582748663-MigrateTestDefinitionKeyToString.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MigrateTestDefinitionKeyToString1731582748663。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1731582748663-MigrateTestDefinitionKeyToString.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1731582748663_MigrateTestDefinitionKeyToString.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class MigrateTestDefinitionKeyToString1731582748663 implements IrreversibleMigration {
	transaction = false as const;

	async up(context: MigrationContext) {
		const { queryRunner, tablePrefix } = context;

		await queryRunner.query(`
			CREATE TABLE "${tablePrefix}TMP_test_definition" ("id" varchar(36) PRIMARY KEY NOT NULL, "name" varchar(255) NOT NULL, "workflowId" varchar(36) NOT NULL, "evaluationWorkflowId" varchar(36), "annotationTagId" varchar(16), "createdAt" datetime(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), "updatedAt" datetime(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), "description" text, CONSTRAINT "FK_${tablePrefix}test_definition_annotation_tag" FOREIGN KEY ("annotationTagId") REFERENCES "annotation_tag_entity" ("id") ON DELETE SET NULL ON UPDATE NO ACTION, CONSTRAINT "FK_${tablePrefix}test_definition_evaluation_workflow_entity" FOREIGN KEY ("evaluationWorkflowId") REFERENCES "workflow_entity" ("id") ON DELETE SET NULL ON UPDATE NO ACTION, CONSTRAINT "FK_${tablePrefix}test_definition_workflow_entity" FOREIGN KEY ("workflowId") REFERENCES "workflow_entity" ("id") ON DELETE CASCADE ON UPDATE NO ACTION);`);
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}TMP_test_definition" SELECT * FROM "${tablePrefix}test_definition";`,
		);
		await queryRunner.query(`DROP TABLE "${tablePrefix}test_definition";`);
		await queryRunner.query(
			`ALTER TABLE "${tablePrefix}TMP_test_definition" RENAME TO "${tablePrefix}test_definition";`,
		);
		await queryRunner.query(
			`CREATE INDEX "idx_${tablePrefix}test_definition_workflow_id" ON "${tablePrefix}test_definition" ("workflowId");`,
		);
		await queryRunner.query(
			`CREATE INDEX "idx_${tablePrefix}test_definition_evaluation_workflow_id" ON "${tablePrefix}test_definition" ("evaluationWorkflowId");`,
		);
	}
}
