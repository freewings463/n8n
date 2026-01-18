"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1681134145996-AddUserActivatedProperty.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../entities/types-db、../migration-types。导出:AddUserActivatedProperty1681134145996。关键函数/方法:up、activatedUsers、JSON_SET、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1681134145996-AddUserActivatedProperty.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1681134145996_AddUserActivatedProperty.py

import type { UserSettings } from '../../entities/types-db';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddUserActivatedProperty1681134145996 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		const activatedUsers = (await queryRunner.query(
			`SELECT DISTINCT sw.userId AS id,
				JSON_SET(COALESCE(u.settings, '{}'), '$.userActivated', JSON('true')) AS settings
			FROM  ${tablePrefix}workflow_statistics AS ws
						JOIN ${tablePrefix}shared_workflow AS sw
							ON ws.workflowId = sw.workflowId
						JOIN ${tablePrefix}role AS r
							ON r.id = sw.roleId
						JOIN ${tablePrefix}user AS u
							ON u.id = sw.userId
			WHERE ws.name = 'production_success'
						AND r.name = 'owner'
						AND r.scope = "workflow"`,
		)) as UserSettings[];

		const updatedUserPromises = activatedUsers.map(async (user) => {
			await queryRunner.query(
				// eslint-disable-next-line @typescript-eslint/restrict-template-expressions
				`UPDATE ${tablePrefix}user SET settings = '${user.settings}' WHERE id = '${user.id}' `,
			);
		});

		await Promise.all(updatedUserPromises);

		if (!activatedUsers.length) {
			await queryRunner.query(
				`UPDATE ${tablePrefix}user SET settings = JSON_SET(COALESCE(settings, '{}'), '$.userActivated', JSON('false'))`,
			);
		} else {
			const activatedUserIds = activatedUsers.map((user) => `'${user.id}'`).join(',');
			await queryRunner.query(
				`UPDATE ${tablePrefix}user SET settings = JSON_SET(COALESCE(settings, '{}'), '$.userActivated', JSON('false')) WHERE id NOT IN (${activatedUserIds})`,
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
