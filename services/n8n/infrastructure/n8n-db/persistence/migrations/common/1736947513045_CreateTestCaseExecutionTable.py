"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1736947513045-CreateTestCaseExecutionTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateTestCaseExecutionTable1736947513045。关键函数/方法:up、column、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1736947513045-CreateTestCaseExecutionTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1736947513045_CreateTestCaseExecutionTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const testCaseExecutionTableName = 'test_case_execution';

export class CreateTestCaseExecutionTable1736947513045 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(testCaseExecutionTableName)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('testRunId').varchar(36).notNull,
				column('pastExecutionId').int, // Might be null if execution was deleted after the test run
				column('executionId').int, // Execution of the workflow under test. Might be null if execution was deleted after the test run
				column('evaluationExecutionId').int, // Execution of the evaluation workflow. Might be null if execution was deleted after the test run, or if the test run was cancelled
				column('status').varchar().notNull,
				column('runAt').timestamp(),
				column('completedAt').timestamp(),
				column('errorCode').varchar(),
				column('errorDetails').json,
				column('metrics').json,
			)
			.withIndexOn('testRunId')
			.withForeignKey('testRunId', {
				tableName: 'test_run',
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('pastExecutionId', {
				tableName: 'execution_entity',
				columnName: 'id',
				onDelete: 'SET NULL',
			})
			.withForeignKey('executionId', {
				tableName: 'execution_entity',
				columnName: 'id',
				onDelete: 'SET NULL',
			})
			.withForeignKey('evaluationExecutionId', {
				tableName: 'execution_entity',
				columnName: 'id',
				onDelete: 'SET NULL',
			}).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(testCaseExecutionTableName);
	}
}
