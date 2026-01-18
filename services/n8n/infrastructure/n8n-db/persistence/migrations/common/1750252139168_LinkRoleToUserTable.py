"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1750252139168-LinkRoleToUserTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:LinkRoleToUserTable1750252139168。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1750252139168-LinkRoleToUserTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1750252139168_LinkRoleToUserTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

/*
 * This migration links the role table to the user table, by adding a new column 'roleSlug'
 * to the user table. It also ensures that all users have a valid role set in the 'roleSlug' column.
 * The migration will insert the global roles that we need into the role table if they do not exist.
 *
 * The old 'role' column in the user table will be removed in a later migration.
 */
export class LinkRoleToUserTable1750252139168 implements ReversibleMigration {
	async up({
		schemaBuilder: { addForeignKey, addColumns, column },
		escape,
		dbType,
		runQuery,
	}: MigrationContext) {
		const roleTableName = escape.tableName('role');
		const userTableName = escape.tableName('user');
		const slugColumn = escape.columnName('slug');
		const roleColumn = escape.columnName('role');
		const roleSlugColumn = escape.columnName('roleSlug');
		const roleTypeColumn = escape.columnName('roleType');
		const systemRoleColumn = escape.columnName('systemRole');

		const isPostgresOrSqlite = dbType === 'postgresdb' || dbType === 'sqlite';
		const upsertQuery = isPostgresOrSqlite
			? `INSERT INTO ${roleTableName} (${slugColumn}, ${roleTypeColumn}, ${systemRoleColumn}) VALUES (:slug, :roleType, :systemRole) ON CONFLICT DO NOTHING`
			: `INSERT IGNORE INTO ${roleTableName} (${slugColumn}, ${roleTypeColumn}, ${systemRoleColumn}) VALUES (:slug, :roleType, :systemRole)`;

		// Make sure that the global roles that we need exist
		for (const role of ['global:owner', 'global:admin', 'global:member']) {
			await runQuery(upsertQuery, {
				slug: role,
				roleType: 'global',
				systemRole: true,
			});
		}

		await addColumns('user', [column('roleSlug').varchar(128).default("'global:member'").notNull]);

		await runQuery(
			`UPDATE ${userTableName} SET ${roleSlugColumn} = ${roleColumn} WHERE ${roleColumn} != ${roleSlugColumn}`,
		);

		// Fallback to 'global:member' for users that do not have a correct role set
		// This should not happen in a correctly set up system, but we want to ensure
		// that all users have a role set, before we add the foreign key constraint
		await runQuery(
			`UPDATE ${userTableName} SET ${roleSlugColumn} = 'global:member' WHERE NOT EXISTS (SELECT 1 FROM ${roleTableName} WHERE ${slugColumn} = ${roleSlugColumn})`,
		);

		await addForeignKey('user', 'roleSlug', ['role', 'slug']);
	}

	async down({ schemaBuilder: { dropForeignKey, dropColumns } }: MigrationContext) {
		await dropForeignKey('user', 'roleSlug', ['role', 'slug']);
		await dropColumns('user', ['roleSlug']);
	}
}
