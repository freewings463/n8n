"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1750252139166-AddScopeTables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddScopeTables1750252139166。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1750252139166-AddScopeTables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1750252139166_AddScopeTables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

/*
 * We introduce a scope table, this will hold all scopes that we know about.
 *
 * The scope table should never be edited by users, on every startup
 * the system will make sure that all scopes that it knows about are stored
 * in here.
 *
 * ColumnName  | Type | Description
 * =================================
 * slug        | Text | Unique identifier of the scope for example: 'project:create'
 * displayName | Text | Name used to display in the UI
 * description | Text | Text describing the scope in more detail of users
 */
export class AddScopeTables1750252139166 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable('scope').withColumns(
			column('slug')
				.varchar(128)
				.primary.notNull.comment('Unique identifier of the scope for example: "project:create"'),
			column('displayName').text.default(null).comment('Name used to display in the UI'),
			column('description')
				.text.default(null)
				.comment('Text describing the scope in more detail of users'),
		);
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable('scope');
	}
}
