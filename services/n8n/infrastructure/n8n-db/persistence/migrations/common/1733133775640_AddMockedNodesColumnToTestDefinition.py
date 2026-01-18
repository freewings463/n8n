"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1733133775640-AddMockedNodesColumnToTestDefinition.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddMockedNodesColumnToTestDefinition1733133775640。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1733133775640-AddMockedNodesColumnToTestDefinition.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1733133775640_AddMockedNodesColumnToTestDefinition.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

// We have to use raw query migration instead of schemaBuilder helpers,
// because the typeorm schema builder implements addColumns by a table recreate for sqlite
// which causes weird issues with the migration
export class AddMockedNodesColumnToTestDefinition1733133775640 implements ReversibleMigration {
	async up({ escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('test_definition');
		const mockedNodesColumnName = escape.columnName('mockedNodes');

		await runQuery(
			`ALTER TABLE ${tableName} ADD COLUMN ${mockedNodesColumnName} JSON DEFAULT ('[]') NOT NULL`,
		);
	}

	async down({ escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('test_definition');
		const columnName = escape.columnName('mockedNodes');

		await runQuery(`ALTER TABLE ${tableName} DROP COLUMN ${columnName}`);
	}
}
