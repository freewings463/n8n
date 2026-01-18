"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1693491613982-ExecutionSoftDelete.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ExecutionSoftDelete1693491613982。关键函数/方法:up、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1693491613982-ExecutionSoftDelete.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1693491613982_ExecutionSoftDelete.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

/**
 * Add an indexed column `deletedAt` to track soft-deleted executions.
 * Add an index on `stoppedAt`, used by executions pruning.
 */
export class ExecutionSoftDelete1693491613982 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, column, createIndex } }: MigrationContext) {
		await addColumns('execution_entity', [column('deletedAt').timestamp()]);
		await createIndex('execution_entity', ['deletedAt']);
		await createIndex('execution_entity', ['stoppedAt']);
	}

	async down({ schemaBuilder: { dropColumns, dropIndex } }: MigrationContext) {
		await dropIndex('execution_entity', ['stoppedAt']);
		await dropIndex('execution_entity', ['deletedAt']);
		await dropColumns('execution_entity', ['deletedAt']);
	}
}
