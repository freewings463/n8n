"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1732549866705-CreateTestRunTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateTestRun1732549866705。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1732549866705-CreateTestRunTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1732549866705_CreateTestRunTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const testRunTableName = 'test_run';

export class CreateTestRun1732549866705 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(testRunTableName)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('testDefinitionId').varchar(36).notNull,
				column('status').varchar().notNull,
				column('runAt').timestamp(),
				column('completedAt').timestamp(),
				column('metrics').json,
			)
			.withIndexOn('testDefinitionId')
			.withForeignKey('testDefinitionId', {
				tableName: 'test_definition',
				columnName: 'id',
				onDelete: 'CASCADE',
			}).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(testRunTableName);
	}
}
