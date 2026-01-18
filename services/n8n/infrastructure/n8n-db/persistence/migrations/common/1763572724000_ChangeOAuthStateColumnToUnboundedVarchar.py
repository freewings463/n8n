"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1763572724000-ChangeOAuthStateColumnToUnboundedVarchar.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的OAuth迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ChangeOAuthStateColumnToUnboundedVarchar1763572724000。关键函数/方法:up、column。用于定义OAuth数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1763572724000-ChangeOAuthStateColumnToUnboundedVarchar.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1763572724000_ChangeOAuthStateColumnToUnboundedVarchar.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

const TABLE_NAME = 'oauth_authorization_codes';
const TEMP_TABLE_NAME = 'temp_oauth_authorization_codes';

export class ChangeOAuthStateColumnToUnboundedVarchar1763572724000
	implements IrreversibleMigration
{
	async up({
		isSqlite,
		isMysql,
		isPostgres,
		escape,
		copyTable,
		queryRunner,
		schemaBuilder: { createTable, column, dropTable },
	}: MigrationContext) {
		const tableName = escape.tableName(TABLE_NAME);

		if (isSqlite) {
			const tempTableName = escape.tableName(TEMP_TABLE_NAME);

			await createTable(TEMP_TABLE_NAME)
				.withColumns(
					column('code').varchar(255).primary.notNull,
					column('clientId').varchar().notNull,
					column('userId').uuid.notNull,
					column('redirectUri').varchar().notNull,
					column('codeChallenge').varchar().notNull,
					column('codeChallengeMethod').varchar(255).notNull,
					column('expiresAt').bigint.notNull.comment('Unix timestamp in milliseconds'),
					column('state').varchar(),
					column('used').bool.notNull.default(false),
				)
				.withForeignKey('clientId', {
					tableName: 'oauth_clients',
					columnName: 'id',
					onDelete: 'CASCADE',
				})
				.withForeignKey('userId', {
					tableName: 'user',
					columnName: 'id',
					onDelete: 'CASCADE',
				}).withTimestamps;

			await copyTable(TABLE_NAME, TEMP_TABLE_NAME);

			await dropTable(TABLE_NAME);

			await queryRunner.query(`ALTER TABLE ${tempTableName} RENAME TO ${tableName};`);
		} else if (isMysql) {
			await queryRunner.query(
				`ALTER TABLE ${tableName} MODIFY COLUMN ${escape.columnName('state')} TEXT;`,
			);
			await queryRunner.query(
				`ALTER TABLE ${tableName} MODIFY COLUMN ${escape.columnName('codeChallenge')} TEXT NOT NULL;`,
			);
			await queryRunner.query(
				`ALTER TABLE ${tableName} MODIFY COLUMN ${escape.columnName('redirectUri')} TEXT NOT NULL;`,
			);
		} else if (isPostgres) {
			await queryRunner.query(
				`ALTER TABLE ${tableName} ALTER COLUMN ${escape.columnName('state')} TYPE VARCHAR,` +
					` ALTER COLUMN ${escape.columnName('codeChallenge')} TYPE VARCHAR,` +
					` ALTER COLUMN ${escape.columnName('redirectUri')} TYPE VARCHAR;`,
			);
		}
	}
}
