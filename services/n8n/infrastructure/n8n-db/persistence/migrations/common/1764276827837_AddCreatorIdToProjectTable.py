"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1764276827837-AddCreatorIdToProjectTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddCreatorIdToProjectTable1764276827837。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1764276827837-AddCreatorIdToProjectTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1764276827837_AddCreatorIdToProjectTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	project: 'project',
	projectRelation: 'project_relation',
} as const;

const FOREIGN_KEY_NAME = 'projects_creatorId_foreign';

export class AddCreatorIdToProjectTable1764276827837 implements ReversibleMigration {
	async up({
		escape,
		schemaBuilder: { addColumns, addForeignKey, column },
		queryRunner,
	}: MigrationContext) {
		await addColumns(table.project, [
			column('creatorId').uuid.comment('ID of the user who created the project'),
		]);

		await addForeignKey(table.project, 'creatorId', ['user', 'id'], FOREIGN_KEY_NAME, 'SET NULL');

		// Populate creatorId for existing personal projects.
		// We can only do this for personal projects as for team projects
		// we don't have a reliable way of knowing who the creator was.
		await queryRunner.query(`
			UPDATE ${escape.tableName(table.project)} AS project
			SET ${escape.columnName('creatorId')} = (
				SELECT pr.${escape.columnName('userId')}
				FROM ${escape.tableName(table.projectRelation)} AS pr
				WHERE pr.${escape.columnName('projectId')} = project.${escape.columnName('id')}
					AND pr.${escape.columnName('role')} = 'project:personalOwner'
				LIMIT 1
			)
			WHERE project.${escape.columnName('type')} = 'personal'
				AND project.${escape.columnName('creatorId')} IS NULL;`);
	}

	async down({ schemaBuilder: { dropColumns, dropForeignKey } }: MigrationContext) {
		await dropForeignKey(table.project, 'creatorId', ['user', 'id'], FOREIGN_KEY_NAME);
		await dropColumns(table.project, ['creatorId']);
	}
}
