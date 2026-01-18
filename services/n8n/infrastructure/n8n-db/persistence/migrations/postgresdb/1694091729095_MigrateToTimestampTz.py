"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1694091729095-MigrateToTimestampTz.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MigrateToTimestampTz1694091729095。关键函数/方法:up、changeColumnType。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1694091729095-MigrateToTimestampTz.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1694091729095_MigrateToTimestampTz.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

const defaultTimestampColumns = ['createdAt', 'updatedAt'];
const tablesWithDefaultTimestamps = [
	'auth_identity',
	'credentials_entity',
	'event_destinations',
	'installed_packages',
	'role',
	'shared_credentials',
	'shared_workflow',
	'tag_entity',
	'user',
	'workflow_entity',
];

const additionalColumns = {
	auth_provider_sync_history: ['endedAt', 'startedAt'],
	execution_entity: ['startedAt', 'stoppedAt', 'waitTill'],
	workflow_statistics: ['latestEvent'],
};

export class MigrateToTimestampTz1694091729095 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const changeColumnType = async (tableName: string, columnName: string, setDefault: boolean) => {
			const alterColumnQuery = `ALTER TABLE "${tablePrefix}${tableName}" ALTER COLUMN "${columnName}"`;
			await queryRunner.query(`${alterColumnQuery} TYPE TIMESTAMP(3) WITH TIME ZONE`);
			if (setDefault)
				await queryRunner.query(`${alterColumnQuery} SET DEFAULT CURRENT_TIMESTAMP(3)`);
		};

		for (const tableName of tablesWithDefaultTimestamps) {
			for (const columnName of defaultTimestampColumns) {
				await changeColumnType(tableName, columnName, true);
			}
		}

		for (const [tableName, columnNames] of Object.entries(additionalColumns)) {
			for (const columnName of columnNames) {
				await changeColumnType(tableName, columnName, false);
			}
		}
	}
}
