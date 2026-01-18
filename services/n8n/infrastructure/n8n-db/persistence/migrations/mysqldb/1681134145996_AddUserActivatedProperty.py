"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1681134145996-AddUserActivatedProperty.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../entities/types-db、../migration-types。导出:AddUserActivatedProperty1681134145996。关键函数/方法:up、activatedUsers、JSON_SET、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1681134145996-AddUserActivatedProperty.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1681134145996_AddUserActivatedProperty.py

import type { UserSettings } from '../../entities/types-db';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddUserActivatedProperty1681134145996 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const activatedUsers = (await queryRunner.query(
			`SELECT DISTINCT sw.userId AS id,
				JSON_SET(COALESCE(u.settings, '{}'), '$.userActivated', true) AS settings
			FROM ${tablePrefix}workflow_statistics AS ws
						JOIN ${tablePrefix}shared_workflow as sw
							ON ws.workflowId = sw.workflowId
						JOIN ${tablePrefix}role AS r
							ON r.id = sw.roleId
						JOIN ${tablePrefix}user AS u
							ON u.id = sw.userId
			WHERE ws.name = 'production_success'
						AND r.name = 'owner'
						AND r.scope = 'workflow'`,
		)) as UserSettings[];

		const updatedUsers = activatedUsers.map(async (user) => {
			/*
				MariaDB returns settings as a string and MySQL as a JSON
			*/
			const userSettings =
				typeof user.settings === 'string' ? user.settings : JSON.stringify(user.settings);
			await queryRunner.query(
				`UPDATE ${tablePrefix}user SET settings = '${userSettings}' WHERE id = '${user.id}' `,
			);
		});

		await Promise.all(updatedUsers);

		if (!activatedUsers.length) {
			await queryRunner.query(
				`UPDATE ${tablePrefix}user SET settings = JSON_SET(COALESCE(settings, '{}'), '$.userActivated', false)`,
			);
		} else {
			const activatedUserIds = activatedUsers.map((user) => `'${user.id}'`).join(',');

			await queryRunner.query(
				`UPDATE ${tablePrefix}user SET settings = JSON_SET(COALESCE(settings, '{}'), '$.userActivated', false) WHERE id NOT IN (${activatedUserIds})`,
			);
		}
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`UPDATE ${tablePrefix}user SET settings = JSON_REMOVE(settings, '$.userActivated')`,
		);
		await queryRunner.query(`UPDATE ${tablePrefix}user SET settings = NULL WHERE settings = '{}'`);
	}
}
