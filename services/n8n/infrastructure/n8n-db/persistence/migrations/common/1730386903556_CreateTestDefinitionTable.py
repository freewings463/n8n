"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1730386903556-CreateTestDefinitionTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateTestDefinitionTable1730386903556。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1730386903556-CreateTestDefinitionTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1730386903556_CreateTestDefinitionTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const testEntityTableName = 'test_definition';

export class CreateTestDefinitionTable1730386903556 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(testEntityTableName)
			.withColumns(
				column('id').int.notNull.primary.autoGenerate,
				column('name').varchar(255).notNull,
				column('workflowId').varchar(36).notNull,
				column('evaluationWorkflowId').varchar(36),
				column('annotationTagId').varchar(16),
			)
			.withIndexOn('workflowId')
			.withIndexOn('evaluationWorkflowId')
			.withForeignKey('workflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('evaluationWorkflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'SET NULL',
			})
			.withForeignKey('annotationTagId', {
				tableName: 'annotation_tag_entity',
				columnName: 'id',
				onDelete: 'SET NULL',
			}).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(testEntityTableName);
	}
}
