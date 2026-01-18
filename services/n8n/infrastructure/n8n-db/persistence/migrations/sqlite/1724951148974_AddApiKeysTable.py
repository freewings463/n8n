"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1724951148974-AddApiKeysTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../../entities、../utils/generators、../migration-types。导出:AddApiKeysTable1724951148974。关键函数/方法:up、UNIQUE、usersWithApiKeys、async、down、MIN、oldestApiKeysPerUser。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1724951148974-AddApiKeysTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1724951148974_AddApiKeysTable.py

import type { ApiKey } from '../../entities';
import { generateNanoId } from '../../utils/generators';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddApiKeysTable1724951148974 implements ReversibleMigration {
	transaction = false as const;

	async up({ queryRunner, tablePrefix, runQuery }: MigrationContext) {
		const tableName = `${tablePrefix}user_api_keys`;

		// Create the table
		await queryRunner.query(`
			CREATE TABLE ${tableName} (
				id VARCHAR(36) PRIMARY KEY NOT NULL,
				"userId" VARCHAR NOT NULL,
				"label" VARCHAR(100) NOT NULL,
				"apiKey" VARCHAR NOT NULL,
				"createdAt" DATETIME(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
				"updatedAt" DATETIME(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
				FOREIGN KEY ("userId") REFERENCES user(id) ON DELETE CASCADE,
				UNIQUE ("userId", label),
				UNIQUE("apiKey")
			);
		`);

		const usersWithApiKeys = (await queryRunner.query(
			`SELECT id, "apiKey" FROM ${tablePrefix}user WHERE "apiKey" IS NOT NULL`,
		)) as Array<Partial<ApiKey>>;

		// Move the apiKey from the users table to the new table
		await Promise.all(
			usersWithApiKeys.map(
				async (user: { id: string; apiKey: string }) =>
					await runQuery(
						`INSERT INTO ${tableName} ("id", "userId", "apiKey", "label") VALUES (:id, :userId, :apiKey, :label)`,
						{
							id: generateNanoId(),
							userId: user.id,
							apiKey: user.apiKey,
							label: 'My API Key',
						},
					),
			),
		);

		// Create temporary table to store the users dropping the api key column
		await queryRunner.query(`
				CREATE TABLE users_new (
					id varchar PRIMARY KEY,
					email VARCHAR(255) UNIQUE,
					"firstName" VARCHAR(32),
					"lastName" VARCHAR(32),
					password VARCHAR,
					"personalizationAnswers" TEXT,
					"createdAt" DATETIME(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
					"updatedAt" DATETIME(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
					settings TEXT,
					disabled BOOLEAN DEFAULT FALSE NOT NULL,
					"mfaEnabled" BOOLEAN DEFAULT FALSE NOT NULL,
					"mfaSecret" TEXT,
					"mfaRecoveryCodes" TEXT,
					role TEXT NOT NULL
			);
		`);

		//  Copy the data from the original users table
		await queryRunner.query(`
			INSERT INTO users_new ("id", "email", "firstName", "lastName", "password", "personalizationAnswers", "createdAt", "updatedAt", "settings", "disabled", "mfaEnabled", "mfaSecret", "mfaRecoveryCodes", "role")
			SELECT "id", "email", "firstName", "lastName", "password", "personalizationAnswers", "createdAt", "updatedAt", "settings", "disabled", "mfaEnabled", "mfaSecret", "mfaRecoveryCodes", "role"
			FROM ${tablePrefix}user;
		`);

		// Drop table with apiKey column
		await queryRunner.query(`DROP TABLE ${tablePrefix}user;`);

		// Rename the temporary table to users
		await queryRunner.query('ALTER TABLE users_new RENAME TO user;');
	}

	async down({
		queryRunner,
		runQuery,
		tablePrefix,
		schemaBuilder: { dropTable, createIndex },
		escape,
	}: MigrationContext) {
		const userApiKeysTable = escape.tableName('user_api_keys');
		const apiKeyColumn = escape.columnName('apiKey');
		const userIdColumn = escape.columnName('userId');
		const idColumn = escape.columnName('id');
		const createdAtColumn = escape.columnName('createdAt');

		const queryToGetUsersApiKeys = `
		SELECT
			${userIdColumn},
			${apiKeyColumn},
			${createdAtColumn}
	FROM
		${userApiKeysTable}
	WHERE
		${createdAtColumn} IN(
			SELECT
				MIN(${createdAtColumn})
				FROM ${userApiKeysTable}
			GROUP BY ${userIdColumn});`;

		const oldestApiKeysPerUser = (await queryRunner.query(queryToGetUsersApiKeys)) as Array<
			Partial<ApiKey>
		>;

		await queryRunner.query(`ALTER TABLE ${tablePrefix}user ADD COLUMN "apiKey" varchar;`);

		await createIndex('user', ['apiKey'], true);

		await Promise.all(
			oldestApiKeysPerUser.map(
				async (user: { userId: string; apiKey: string }) =>
					await runQuery(
						`UPDATE ${tablePrefix}user SET ${apiKeyColumn} = :apiKey WHERE ${idColumn} = :userId`,
						user,
					),
			),
		);

		await dropTable('user_api_keys');
	}
}
