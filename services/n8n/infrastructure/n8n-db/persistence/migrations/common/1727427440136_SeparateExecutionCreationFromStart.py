"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1727427440136-SeparateExecutionCreationFromStart.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:SeparateExecutionCreationFromStart1727427440136。关键函数/方法:up、column、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1727427440136-SeparateExecutionCreationFromStart.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1727427440136_SeparateExecutionCreationFromStart.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class SeparateExecutionCreationFromStart1727427440136 implements ReversibleMigration {
	async up({
		schemaBuilder: { addColumns, column, dropNotNull },
		runQuery,
		escape,
	}: MigrationContext) {
		await addColumns('execution_entity', [
			column('createdAt').notNull.timestamp().default('NOW()'),
		]);

		await dropNotNull('execution_entity', 'startedAt');

		const executionEntity = escape.tableName('execution_entity');
		const createdAt = escape.columnName('createdAt');
		const startedAt = escape.columnName('startedAt');

		// inaccurate for pre-migration rows but prevents `createdAt` from being nullable
		await runQuery(`UPDATE ${executionEntity} SET ${createdAt} = ${startedAt};`);
	}

	async down({ schemaBuilder: { dropColumns, addNotNull } }: MigrationContext) {
		await dropColumns('execution_entity', ['createdAt']);
		await addNotNull('execution_entity', 'startedAt');
	}
}
