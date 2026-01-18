"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1700571993961-AddGlobalAdminRole.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:n8n-workflow；本地:../migration-types。导出:AddGlobalAdminRole1700571993961。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1700571993961-AddGlobalAdminRole.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1700571993961_AddGlobalAdminRole.py

import { UnexpectedError } from 'n8n-workflow';

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddGlobalAdminRole1700571993961 implements ReversibleMigration {
	async up({ escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('role');

		await runQuery(`INSERT INTO ${tableName} (name, scope) VALUES (:name, :scope)`, {
			name: 'admin',
			scope: 'global',
		});
	}

	async down({ escape, runQuery }: MigrationContext) {
		const roleTableName = escape.tableName('role');
		const userTableName = escape.tableName('user');

		const adminRoleIdResult = await runQuery<Array<{ id: number }>>(
			`SELECT id FROM ${roleTableName} WHERE name = :name AND scope = :scope`,
			{
				name: 'admin',
				scope: 'global',
			},
		);

		const memberRoleIdResult = await runQuery<Array<{ id: number }>>(
			`SELECT id FROM ${roleTableName} WHERE name = :name AND scope = :scope`,
			{
				name: 'member',
				scope: 'global',
			},
		);

		const adminRoleId = adminRoleIdResult[0]?.id;
		if (adminRoleId === undefined) {
			// Couldn't find admin role. It's a bit odd but it means we don't
			// have anything to do.
			return;
		}

		const memberRoleId = memberRoleIdResult[0]?.id;
		if (!memberRoleId) {
			throw new UnexpectedError('Could not find global member role!');
		}

		await runQuery(
			`UPDATE ${userTableName} SET globalRoleId = :memberRoleId WHERE globalRoleId = :adminRoleId`,
			{
				memberRoleId,
				adminRoleId,
			},
		);

		await runQuery(`DELETE FROM ${roleTableName} WHERE name = :name AND scope = :scope`, {
			name: 'admin',
			scope: 'global',
		});
	}
}
