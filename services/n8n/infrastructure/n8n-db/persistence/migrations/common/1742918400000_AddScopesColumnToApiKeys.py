"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1742918400000-AddScopesColumnToApiKeys.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:@n8n/permissions；本地:../../constants、../../entities、../migration-types。导出:AddScopesColumnToApiKeys1742918400000。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1742918400000-AddScopesColumnToApiKeys.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1742918400000_AddScopesColumnToApiKeys.py

import type { GlobalRole } from '@n8n/permissions';
import { getApiKeyScopesForRole } from '@n8n/permissions';

import { GLOBAL_ROLES } from '../../constants';
import { ApiKey } from '../../entities';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

type ApiKeyWithRole = { id: string; role: GlobalRole };

export class AddScopesColumnToApiKeys1742918400000 implements ReversibleMigration {
	async up({
		runQuery,
		escape,
		queryRunner,
		schemaBuilder: { addColumns, column },
	}: MigrationContext) {
		await addColumns('user_api_keys', [column('scopes').json]);

		const userApiKeysTable = escape.tableName('user_api_keys');
		const userTable = escape.tableName('user');
		const idColumn = escape.columnName('id');
		const userIdColumn = escape.columnName('userId');
		const roleColumn = escape.columnName('role');

		const apiKeysWithRoles = await runQuery<ApiKeyWithRole[]>(
			`SELECT ${userApiKeysTable}.${idColumn} AS id, ${userTable}.${roleColumn} AS role FROM ${userApiKeysTable} JOIN ${userTable} ON ${userTable}.${idColumn} = ${userApiKeysTable}.${userIdColumn}`,
		);

		for (const { id, role } of apiKeysWithRoles) {
			const dbRole = GLOBAL_ROLES[role];
			const scopes = getApiKeyScopesForRole({
				role: dbRole,
			});
			await queryRunner.manager.update(ApiKey, { id }, { scopes });
		}
	}

	async down({ schemaBuilder: { dropColumns } }: MigrationContext) {
		await dropColumns('user_api_keys', ['scopes']);
	}
}
