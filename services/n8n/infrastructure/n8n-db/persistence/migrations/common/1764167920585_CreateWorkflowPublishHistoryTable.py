"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1764167920585-CreateWorkflowPublishHistoryTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateWorkflowPublishHistoryTable1764167920585。关键函数/方法:up、column、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1764167920585-CreateWorkflowPublishHistoryTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1764167920585_CreateWorkflowPublishHistoryTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const workflowPublishHistoryTableName = 'workflow_publish_history';

export class CreateWorkflowPublishHistoryTable1764167920585 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column }, escape, runQuery }: MigrationContext) {
		await createTable(workflowPublishHistoryTableName)
			.withColumns(
				column('id').int.primary.autoGenerate2,
				column('workflowId').varchar(36).notNull,
				column('versionId').varchar(36).notNull,
				column('event')
					.varchar(36)
					.notNull.comment(
						'Type of history record: activated (workflow is now active), deactivated (workflow is now inactive)',
					),
				column('userId').uuid,
			)
			.withCreatedAt.withIndexOn(['workflowId', 'versionId'])
			.withForeignKey('workflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('versionId', {
				tableName: 'workflow_history',
				columnName: 'versionId',
				onDelete: 'CASCADE',
			})
			.withForeignKey('userId', {
				tableName: 'user',
				columnName: 'id',
				onDelete: 'SET NULL',
			})
			.withEnumCheck('event', ['activated', 'deactivated']);

		const escapedWphTableName = escape.tableName(workflowPublishHistoryTableName);
		const workflowEntityTableName = escape.tableName('workflow_entity');
		const id = escape.columnName('id');
		const activeVersionId = escape.columnName('activeVersionId');
		const workflowId = escape.columnName('workflowId');
		const versionId = escape.columnName('versionId');
		const event = escape.columnName('event');
		const updatedAt = escape.columnName('updatedAt');
		const createdAt = escape.columnName('createdAt');

		await runQuery(
			`INSERT INTO ${escapedWphTableName} (${workflowId}, ${versionId}, ${event}, ${createdAt})
				SELECT we.${id}, we.${activeVersionId}, 'activated', we.${updatedAt}
				FROM ${workflowEntityTableName} we
				WHERE we.${activeVersionId} IS NOT NULL`,
		);
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(workflowPublishHistoryTableName);
	}
}
