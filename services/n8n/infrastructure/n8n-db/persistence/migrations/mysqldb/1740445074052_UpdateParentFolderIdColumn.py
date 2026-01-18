"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1740445074052-UpdateParentFolderIdColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:UpdateParentFolderIdColumn1740445074052。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1740445074052-UpdateParentFolderIdColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1740445074052_UpdateParentFolderIdColumn.py

import type { BaseMigration, MigrationContext } from '../migration-types';

export class UpdateParentFolderIdColumn1740445074052 implements BaseMigration {
	async up({ escape, queryRunner }: MigrationContext) {
		const workflowTableName = escape.tableName('workflow_entity');
		const folderTableName = escape.tableName('folder');
		const parentFolderIdColumn = escape.columnName('parentFolderId');
		const idColumn = escape.columnName('id');

		await queryRunner.query(
			`ALTER TABLE ${workflowTableName} ADD CONSTRAINT fk_workflow_parent_folder FOREIGN KEY (${parentFolderIdColumn}) REFERENCES ${folderTableName}(${idColumn}) ON DELETE CASCADE`,
		);
	}
}
