"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1753953244168-LinkRoleToProjectRelationTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../../constants、../migration-types。导出:LinkRoleToProjectRelationTable1753953244168。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1753953244168-LinkRoleToProjectRelationTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1753953244168_LinkRoleToProjectRelationTable.py

import { PROJECT_ROLES, PROJECT_VIEWER_ROLE } from '../../constants';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

/*
 * This migration links the role table to the project relation table, by adding a new foreign key on the 'role' column
 * It also ensures that all project relations have a valid role set in the 'role' column.
 * The migration will insert the project roles that we need into the role table if they do not exist.
 */

export class LinkRoleToProjectRelationTable1753953244168 implements ReversibleMigration {
	async up({ schemaBuilder: { addForeignKey }, escape, dbType, runQuery }: MigrationContext) {
		const roleTableName = escape.tableName('role');
		const projectRelationTableName = escape.tableName('project_relation');
		const slugColumn = escape.columnName('slug');
		const roleColumn = escape.columnName('role');
		const roleTypeColumn = escape.columnName('roleType');
		const systemRoleColumn = escape.columnName('systemRole');

		const isPostgresOrSqlite = dbType === 'postgresdb' || dbType === 'sqlite';
		const query = isPostgresOrSqlite
			? `INSERT INTO ${roleTableName} (${slugColumn}, ${roleTypeColumn}, ${systemRoleColumn}) VALUES (:slug, :roleType, :systemRole) ON CONFLICT DO NOTHING`
			: `INSERT IGNORE INTO ${roleTableName} (${slugColumn}, ${roleTypeColumn}, ${systemRoleColumn}) VALUES (:slug, :roleType, :systemRole)`;

		// Make sure that the project roles that we need exist
		for (const role of Object.values(PROJECT_ROLES)) {
			await runQuery(query, {
				slug: role.slug,
				roleType: role.roleType,
				systemRole: role.systemRole,
			});
		}

		// Fallback to 'project:viewer' for users that do not have a correct role set
		// This should not happen in a correctly set up system, but we want to ensure
		// that all users have a role set, before we add the foreign key constraint
		await runQuery(
			`UPDATE ${projectRelationTableName} SET ${roleColumn} = '${PROJECT_VIEWER_ROLE.slug}' WHERE NOT EXISTS (SELECT 1 FROM ${roleTableName} WHERE ${slugColumn} = ${roleColumn})`,
		);

		await addForeignKey('project_relation', 'role', ['role', 'slug']);
	}

	async down({ schemaBuilder: { dropForeignKey } }: MigrationContext) {
		await dropForeignKey('project_relation', 'role', ['role', 'slug']);
	}
}
