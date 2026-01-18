"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1764689388394-AddDynamicCredentialEntryTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddDynamicCredentialEntryTable1764689388394。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1764689388394-AddDynamicCredentialEntryTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1764689388394_AddDynamicCredentialEntryTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const tableName = 'dynamic_credential_entry';

export class AddDynamicCredentialEntryTable1764689388394 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(tableName)
			.withColumns(
				column('credential_id').varchar(16).primary.notNull,
				column('subject_id').varchar(16).primary.notNull,
				column('resolver_id').varchar(16).primary.notNull,
				column('data').text.notNull,
			)
			.withTimestamps.withForeignKey('credential_id', {
				tableName: 'credentials_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('resolver_id', {
				tableName: 'dynamic_credential_resolver',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withIndexOn(['subject_id'])
			.withIndexOn(['resolver_id']);
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(tableName);
	}
}
