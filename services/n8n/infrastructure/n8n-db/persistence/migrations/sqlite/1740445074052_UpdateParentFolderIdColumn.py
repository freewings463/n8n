"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1740445074052-UpdateParentFolderIdColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:./1740445074052-UpdateParentFolderIdColumn、../migration-types。导出:UpdateParentFolderIdColumn1740445074052。关键函数/方法:up、column。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1740445074052-UpdateParentFolderIdColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1740445074052_UpdateParentFolderIdColumn.py

import type { UpdateParentFolderIdColumn1740445074052 as BaseMigration } from './1740445074052-UpdateParentFolderIdColumn';
import type { MigrationContext } from '../migration-types';

export class UpdateParentFolderIdColumn1740445074052 implements BaseMigration {
	transaction = false as const;

	async up({
		queryRunner,
		copyTable,
		schemaBuilder: { createTable, column },
		tablePrefix,
	}: MigrationContext) {
		await createTable('temp_workflow_entity')
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('name').varchar(128).notNull,
				column('active').bool.notNull,
				column('nodes').json,
				column('connections').json,
				column('settings').json,
				column('staticData').json,
				column('pinData').json,
				column('versionId').varchar(36),
				column('triggerCount').int.default(0),
				column('meta').json,
				column('parentFolderId').varchar(36).default(null),
			)
			.withForeignKey('parentFolderId', {
				tableName: 'folder',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withIndexOn(['name'], false).withTimestamps;

		const columns = [
			'id',
			'name',
			'active',
			'nodes',
			'connections',
			'settings',
			'staticData',
			'pinData',
			'versionId',
			'triggerCount',
			'meta',
			'parentFolderId',
			'createdAt',
			'updatedAt',
		];

		await copyTable(`${tablePrefix}workflow_entity`, 'temp_workflow_entity', columns);

		await queryRunner.query(`DROP TABLE "${tablePrefix}workflow_entity";`);

		await queryRunner.query(
			`ALTER TABLE "temp_workflow_entity" RENAME TO "${tablePrefix}workflow_entity";`,
		);
	}
}
