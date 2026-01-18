"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1760020838000-UniqueRoleNames.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../../entities、../migration-types。导出:UniqueRoleNames1760020838000。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1760020838000-UniqueRoleNames.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1760020838000_UniqueRoleNames.py

import type { Role } from '../../entities';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class UniqueRoleNames1760020838000 implements ReversibleMigration {
	async up({ isMysql, escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('role');
		const displayNameColumn = escape.columnName('displayName');
		const slugColumn = escape.columnName('slug');
		const createdAtColumn = escape.columnName('createdAt');
		const allRoles: Array<Pick<Role, 'slug' | 'displayName'>> = await runQuery(
			`SELECT ${slugColumn}, ${displayNameColumn} FROM ${tableName} ORDER BY ${displayNameColumn}, ${createdAtColumn} ASC`,
		);

		// Group roles by displayName in memory
		const groupedByName = new Map<string, Array<Pick<Role, 'slug' | 'displayName'>>>();

		for (const role of allRoles) {
			const existing = groupedByName.get(role.displayName) || [];
			existing.push(role);
			groupedByName.set(role.displayName, existing);
		}

		for (const [_, roles] of groupedByName.entries()) {
			if (roles.length > 1) {
				const duplicates = roles.slice(1);
				let index = 2;
				for (const role of duplicates.values()) {
					let newDisplayName = `${role.displayName} ${index}`;
					while (allRoles.some((r) => r.displayName === newDisplayName)) {
						index++;
						newDisplayName = `${role.displayName} ${index}`;
					}
					await runQuery(
						`UPDATE ${tableName} SET ${displayNameColumn} = :displayName WHERE ${slugColumn} = :slug`,
						{
							displayName: newDisplayName,
							slug: role.slug,
						},
					);
					index++;
				}
			}
		}

		const indexName = escape.indexName('UniqueRoleDisplayName');
		// MySQL cannot create an index on a column with a type of TEXT or BLOB without a length limit
		// The (100) specifies the maximum length of the index key
		// meaning that only the first 100 characters of the displayName column will be used for indexing
		// But since in our DTOs we limit the displayName to 100 characters, we can safely use this prefix length
		await runQuery(
			isMysql
				? `CREATE UNIQUE INDEX ${indexName} ON ${tableName} (${displayNameColumn}(100))`
				: `CREATE UNIQUE INDEX ${indexName} ON ${tableName} (${displayNameColumn})`,
		);
	}

	async down({ isMysql, escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('role');
		const indexName = escape.indexName('UniqueRoleDisplayName');
		await runQuery(
			isMysql ? `ALTER TABLE ${tableName} DROP INDEX ${indexName}` : `DROP INDEX ${indexName}`,
		);
	}
}
