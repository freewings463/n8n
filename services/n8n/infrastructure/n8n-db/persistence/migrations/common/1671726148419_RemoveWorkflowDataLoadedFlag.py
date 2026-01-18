"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1671726148419-RemoveWorkflowDataLoadedFlag.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../entities/types-db、../migration-types。导出:RemoveWorkflowDataLoadedFlag1671726148419。关键函数/方法:up、async、runQuery、VALUES、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1671726148419-RemoveWorkflowDataLoadedFlag.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1671726148419_RemoveWorkflowDataLoadedFlag.py

import { StatisticsNames } from '../../entities/types-db';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class RemoveWorkflowDataLoadedFlag1671726148419 implements ReversibleMigration {
	async up({ escape, dbType, runQuery }: MigrationContext) {
		const workflowTableName = escape.tableName('workflow_entity');
		const statisticsTableName = escape.tableName('workflow_statistics');
		const columnName = escape.columnName('dataLoaded');

		// If any existing workflow has dataLoaded set to true, insert the relevant information to the statistics table
		const workflowIds: Array<{ id: number; dataLoaded: boolean }> = await runQuery(
			`SELECT id, ${columnName} FROM ${workflowTableName}`,
		);

		const now =
			dbType === 'sqlite' ? "STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')" : 'CURRENT_TIMESTAMP(3)';

		await Promise.all(
			workflowIds.map(
				async ({ id, dataLoaded }) =>
					await (dataLoaded &&
						runQuery(
							`INSERT INTO ${statisticsTableName}
						(${escape.columnName('workflowId')}, name, count, ${escape.columnName('latestEvent')})
						VALUES (:id, :name, 1, ${now})`,
							{ id, name: StatisticsNames.dataLoaded },
						)),
			),
		);

		await runQuery(`ALTER TABLE ${workflowTableName} DROP COLUMN ${columnName}`);
	}

	async down({ escape, runQuery }: MigrationContext) {
		const workflowTableName = escape.tableName('workflow_entity');
		const statisticsTableName = escape.tableName('workflow_statistics');
		const columnName = escape.columnName('dataLoaded');

		await runQuery(
			`ALTER TABLE ${workflowTableName} ADD COLUMN ${columnName} BOOLEAN DEFAULT false`,
		);

		// Search through statistics for any workflows that have the dataLoaded stat
		const workflowsIds: Array<{ workflowId: string }> = await runQuery(
			`SELECT ${escape.columnName('workflowId')} FROM ${statisticsTableName} WHERE name = :name`,
			{ name: StatisticsNames.dataLoaded },
		);

		await Promise.all(
			workflowsIds.map(
				async ({ workflowId }) =>
					await runQuery(`UPDATE ${workflowTableName} SET ${columnName} = true WHERE id = :id`, {
						id: workflowId,
					}),
			),
		);

		await runQuery(`DELETE FROM ${statisticsTableName} WHERE name = :name`, {
			name: StatisticsNames.dataLoaded,
		});
	}
}
