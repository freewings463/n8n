"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1726606152711-CreateProcessedDataTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateProcessedDataTable1726606152711。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1726606152711-CreateProcessedDataTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1726606152711_CreateProcessedDataTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const processedDataTableName = 'processed_data';

export class CreateProcessedDataTable1726606152711 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(processedDataTableName)
			.withColumns(
				column('workflowId').varchar(36).notNull.primary,
				column('value').varchar(255).notNull,
				column('context').varchar(255).notNull.primary,
			)
			.withForeignKey('workflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			}).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(processedDataTableName);
	}
}
