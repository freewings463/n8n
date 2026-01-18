"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1693554410387-DisallowOrphanExecutions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:DisallowOrphanExecutions1693554410387。关键函数/方法:up、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1693554410387-DisallowOrphanExecutions.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1693554410387_DisallowOrphanExecutions.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class DisallowOrphanExecutions1693554410387 implements ReversibleMigration {
	/**
	 * Ensure all executions point to a workflow.
	 */
	async up({ escape, schemaBuilder: { addNotNull }, runQuery }: MigrationContext) {
		const executionEntity = escape.tableName('execution_entity');
		const workflowId = escape.columnName('workflowId');

		await runQuery(`DELETE FROM ${executionEntity} WHERE ${workflowId} IS NULL;`);

		await addNotNull('execution_entity', 'workflowId');
	}

	/**
	 * Reversal excludes restoring deleted rows.
	 */
	async down({ schemaBuilder: { dropNotNull } }: MigrationContext) {
		await dropNotNull('execution_entity', 'workflowId');
	}
}
