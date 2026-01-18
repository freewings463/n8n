"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1766500000000-ExpandInsightsWorkflowIdLength.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ExpandInsightsWorkflowIdLength1766500000000。关键函数/方法:up。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1766500000000-ExpandInsightsWorkflowIdLength.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1766500000000_ExpandInsightsWorkflowIdLength.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

/**
 * This migration expands the workflowId column from varchar(16) to varchar(36)
 * to accommodate frontend-generated workflow IDs which are 21 characters long.
 *
 * Background:
 * - The original analytics/insights tables were created with workflowId as varchar(16)
 * - This matched the backend-generated ID length at the time
 * - PR #21955 introduced frontend-generated workflow IDs using nanoid() which defaults to 21 chars
 * - This caused insights to fail for workflows with 21-char IDs
 *
 * The fix aligns with the codebase standard of varchar(36) for workflowId columns.
 */
export class ExpandInsightsWorkflowIdLength1766500000000 implements IrreversibleMigration {
	async up({ escape, queryRunner }: MigrationContext) {
		const tableName = escape.tableName('insights_metadata');
		const columnName = escape.columnName('workflowId');

		await queryRunner.query(
			`ALTER TABLE ${tableName} ALTER COLUMN ${columnName} TYPE VARCHAR(36);`,
		);
	}
}
