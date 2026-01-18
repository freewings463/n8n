"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1692967111175-CreateWorkflowHistoryTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateWorkflowHistoryTable1692967111175。关键函数/方法:up、column、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1692967111175-CreateWorkflowHistoryTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1692967111175_CreateWorkflowHistoryTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const tableName = 'workflow_history';

export class CreateWorkflowHistoryTable1692967111175 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(tableName)
			.withColumns(
				column('versionId').varchar(36).primary.notNull,
				column('workflowId').varchar(36).notNull,
				column('nodes').text.notNull,
				column('connections').text.notNull,
				column('authors').varchar(255).notNull,
			)
			.withTimestamps.withIndexOn('workflowId')
			.withForeignKey('workflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			});
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(tableName);
	}
}
