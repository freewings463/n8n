"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1760314000000-CreateWorkflowDependencyTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateWorkflowDependencyTable1760314000000。关键函数/方法:up、column、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1760314000000-CreateWorkflowDependencyTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1760314000000_CreateWorkflowDependencyTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateWorkflowDependencyTable1760314000000 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable('workflow_dependency')
			.withColumns(
				column('id').int.primary.autoGenerate2,
				column('workflowId').varchar(36).notNull,
				column('workflowVersionId').int.notNull.comment('Version of the workflow'),
				column('dependencyType')
					.varchar(32)
					.notNull.comment(
						'Type of dependency: "credential", "nodeType", "webhookPath", or "workflowCall"',
					),
				column('dependencyKey').varchar(255).notNull.comment('ID or name of the dependency'),
				column('dependencyInfo')
					.varchar(255)
					.comment('Additional info about the dependency, interpreted based on type'),
				column('indexVersionId')
					.smallint.notNull.default(1)
					.comment('Version of the index structure'),
			)
			.withForeignKey('workflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withIndexOn(['workflowId'])
			.withIndexOn(['dependencyType'])
			.withIndexOn(['dependencyKey']).withCreatedAt;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable('workflow_dependency');
	}
}
