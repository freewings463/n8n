"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1745322634000-CleanEvaluations.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ClearEvaluation1745322634000。关键函数/方法:up、column。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1745322634000-CleanEvaluations.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1745322634000_CleanEvaluations.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

const testRunTableName = 'test_run';
const testCaseExecutionTableName = 'test_case_execution';
export class ClearEvaluation1745322634000 implements IrreversibleMigration {
	async up({
		schemaBuilder: { dropTable, column, createTable },
		queryRunner,
		tablePrefix,
		isSqlite,
		isPostgres,
		isMysql,
	}: MigrationContext) {
		// Drop test_metric, test_definition
		await dropTable(testCaseExecutionTableName);
		await dropTable(testRunTableName);
		await dropTable('test_metric');
		if (isSqlite) {
			await queryRunner.query(`DROP TABLE IF EXISTS ${tablePrefix}test_definition;`);
		} else if (isPostgres) {
			await queryRunner.query(`DROP TABLE IF EXISTS ${tablePrefix}test_definition CASCADE;`);
		} else if (isMysql) {
			await queryRunner.query(`DROP TABLE IF EXISTS ${tablePrefix}test_definition CASCADE;`);
		}

		await createTable(testRunTableName)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('workflowId').varchar(36).notNull,
				column('status').varchar().notNull,
				column('errorCode').varchar(),
				column('errorDetails').json,
				column('runAt').timestamp(),
				column('completedAt').timestamp(),
				column('metrics').json,
			)
			.withIndexOn('workflowId')
			.withForeignKey('workflowId', {
				tableName: 'workflow_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			}).withTimestamps;

		await createTable(testCaseExecutionTableName)
			.withColumns(
				column('id').varchar(36).primary.notNull,
				column('testRunId').varchar(36).notNull,
				column('executionId').int, // Execution of the workflow under test. Might be null if execution was deleted after the test run
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
			.withForeignKey('executionId', {
				tableName: 'execution_entity',
				columnName: 'id',
				onDelete: 'SET NULL',
			}).withTimestamps;
	}
}
