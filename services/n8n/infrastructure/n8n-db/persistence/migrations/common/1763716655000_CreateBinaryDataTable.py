"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1763716655000-CreateBinaryDataTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateBinaryDataTable1763716655000。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1763716655000-CreateBinaryDataTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1763716655000_CreateBinaryDataTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const tableName = 'binary_data';

export class CreateBinaryDataTable1763716655000 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(tableName)
			.withColumns(
				column('fileId').uuid.primary.notNull,
				column('sourceType')
					.varchar(50)
					.notNull.comment("Source the file belongs to, e.g. 'execution'"),
				column('sourceId').varchar(255).notNull.comment('ID of the source, e.g. execution ID'),
				column('data').binary.notNull.comment('Raw, not base64 encoded'),
				column('mimeType').varchar(255),
				column('fileName').varchar(255),
				column('fileSize').int.notNull.comment('In bytes'),
			)
			.withEnumCheck('sourceType', ['execution', 'chat_message_attachment'])
			.withIndexOn(['sourceType', 'sourceId']).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(tableName);
	}
}
