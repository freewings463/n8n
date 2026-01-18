"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1765448186933-BackfillMissingWorkflowHistoryRecords.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:BackfillMissingWorkflowHistoryRecords1765448186933。关键函数/方法:up。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1765448186933-BackfillMissingWorkflowHistoryRecords.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1765448186933_BackfillMissingWorkflowHistoryRecords.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

// Some users still have missing workflow history records after pulling workflows using source control feature
export class BackfillMissingWorkflowHistoryRecords1765448186933 implements IrreversibleMigration {
	async up({ escape, runQuery }: MigrationContext) {
		const workflowTable = escape.tableName('workflow_entity');
		const historyTable = escape.tableName('workflow_history');
		const versionIdColumn = escape.columnName('versionId');
		const idColumn = escape.columnName('id');
		const workflowIdColumn = escape.columnName('workflowId');
		const nodesColumn = escape.columnName('nodes');
		const connectionsColumn = escape.columnName('connections');
		const authorsColumn = escape.columnName('authors');
		const createdAtColumn = escape.columnName('createdAt');
		const updatedAtColumn = escape.columnName('updatedAt');

		await runQuery(
			`
            INSERT INTO ${historyTable} (
                ${versionIdColumn},
                ${workflowIdColumn},
                ${authorsColumn},
                ${nodesColumn},
                ${connectionsColumn},
                ${createdAtColumn},
                ${updatedAtColumn}
            )
            SELECT
                w.${versionIdColumn},
                w.${idColumn},
                :authors,
                w.${nodesColumn},
                w.${connectionsColumn},
                :createdAt,
                :updatedAt
            FROM ${workflowTable} w
            LEFT JOIN ${historyTable} wh
                ON w.${versionIdColumn} = wh.${versionIdColumn}
            WHERE wh.${versionIdColumn} IS NULL
            `,
			{
				authors: 'system migration',
				createdAt: new Date(),
				updatedAt: new Date(),
			},
		);
	}
}
