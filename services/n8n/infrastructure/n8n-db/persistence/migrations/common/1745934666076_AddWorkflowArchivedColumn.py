"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1745934666076-AddWorkflowArchivedColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddWorkflowArchivedColumn1745934666076。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1745934666076-AddWorkflowArchivedColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1745934666076_AddWorkflowArchivedColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const columnName = 'isArchived';
const tableName = 'workflow_entity';

export class AddWorkflowArchivedColumn1745934666076 implements ReversibleMigration {
	async up({ escape, runQuery }: MigrationContext) {
		const escapedTableName = escape.tableName(tableName);
		const escapedColumnName = escape.columnName(columnName);

		await runQuery(
			`ALTER TABLE ${escapedTableName} ADD COLUMN ${escapedColumnName} BOOLEAN NOT NULL DEFAULT FALSE`,
		);
	}

	async down({ escape, runQuery }: MigrationContext) {
		const escapedTableName = escape.tableName(tableName);
		const escapedColumnName = escape.columnName(columnName);

		await runQuery(`ALTER TABLE ${escapedTableName} DROP COLUMN ${escapedColumnName}`);
	}
}
