"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1763047800000-AddActiveVersionIdColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddActiveVersionIdColumn1763047800000。关键函数/方法:up、down、backFillHistoryRecords。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1763047800000-AddActiveVersionIdColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1763047800000_AddActiveVersionIdColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const WORKFLOWS_TABLE_NAME = 'workflow_entity';
const WORKFLOW_HISTORY_TABLE_NAME = 'workflow_history';

export class AddActiveVersionIdColumn1763047800000 implements ReversibleMigration {
	async up({
		schemaBuilder: { addColumns, column, addForeignKey },
		queryRunner,
		escape,
		runQuery,
	}: MigrationContext) {
		const workflowsTableName = escape.tableName(WORKFLOWS_TABLE_NAME);

		await addColumns(WORKFLOWS_TABLE_NAME, [column('activeVersionId').varchar(36)]);

		await addForeignKey(
			WORKFLOWS_TABLE_NAME,
			'activeVersionId',
			[WORKFLOW_HISTORY_TABLE_NAME, 'versionId'],
			undefined,
			'RESTRICT',
		);

		// Fix for ADO-4517: some users pulled workflows to prod instances and ended up having missing records
		// Run AFTER adding column/FK to avoid CASCADE DELETE
		await this.backFillHistoryRecords(runQuery, escape);

		// For existing ACTIVE workflows, set activeVersionId = versionId
		const versionIdColumn = escape.columnName('versionId');
		const activeColumn = escape.columnName('active');
		const activeVersionIdColumn = escape.columnName('activeVersionId');

		await queryRunner.query(
			`UPDATE ${workflowsTableName}
			 SET ${activeVersionIdColumn} = ${versionIdColumn}
			 WHERE ${activeColumn} = true`,
		);
	}

	async down({ schemaBuilder: { dropColumns, dropForeignKey } }: MigrationContext) {
		await dropForeignKey(WORKFLOWS_TABLE_NAME, 'activeVersionId', [
			WORKFLOW_HISTORY_TABLE_NAME,
			'versionId',
		]);
		await dropColumns(WORKFLOWS_TABLE_NAME, ['activeVersionId']);
	}

	// Create workflow_history records for workflows missing them
	async backFillHistoryRecords(
		runQuery: MigrationContext['runQuery'],
		escape: MigrationContext['escape'],
	) {
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
