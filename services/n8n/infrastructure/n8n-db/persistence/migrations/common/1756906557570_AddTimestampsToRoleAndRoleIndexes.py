"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1756906557570-AddTimestampsToRoleAndRoleIndexes.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../dsl/column、../migration-types。导出:AddTimestampsToRoleAndRoleIndexes1756906557570。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1756906557570-AddTimestampsToRoleAndRoleIndexes.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1756906557570_AddTimestampsToRoleAndRoleIndexes.py

import { Column } from '../dsl/column';
import type { IrreversibleMigration, MigrationContext } from '../migration-types';

const ROLE_TABLE_NAME = 'role';
const PROJECT_RELATION_TABLE_NAME = 'project_relation';
const USER_TABLE_NAME = 'user';
const PROJECT_RELATION_ROLE_IDX_NAME = 'project_relation_role_idx';
const PROJECT_RELATION_ROLE_PROJECT_IDX_NAME = 'project_relation_role_project_idx';
const USER_ROLE_IDX_NAME = 'user_role_idx';

export class AddTimestampsToRoleAndRoleIndexes1756906557570 implements IrreversibleMigration {
	async up({ schemaBuilder, queryRunner, tablePrefix }: MigrationContext) {
		// This loads the table metadata from the database and
		// feeds the query runners cache with the table metadata
		// Not doing this, seems to get TypeORM to wrongfully try to
		// add the columns twice in the same statement.
		await queryRunner.getTable(`${tablePrefix}${USER_TABLE_NAME}`);

		await schemaBuilder.addColumns(ROLE_TABLE_NAME, [
			new Column('createdAt').timestampTimezone().notNull.default('NOW()'),
			new Column('updatedAt').timestampTimezone().notNull.default('NOW()'),
		]);

		// This index should allow us to efficiently query project relations by their role
		// This will be used for counting how many users have a specific project role
		await schemaBuilder.createIndex(
			PROJECT_RELATION_TABLE_NAME,
			['role'],
			false,
			PROJECT_RELATION_ROLE_IDX_NAME,
		);

		// This index should allow us to efficiently query project relations by their role and project
		// This will be used for counting how many users in a specific project have a specific project role
		await schemaBuilder.createIndex(
			PROJECT_RELATION_TABLE_NAME,
			['projectId', 'role'],
			false,
			PROJECT_RELATION_ROLE_PROJECT_IDX_NAME,
		);

		// This index should allow us to efficiently query users by their role slug
		// This will be used for counting how many users have a specific global role
		await schemaBuilder.createIndex(USER_TABLE_NAME, ['roleSlug'], false, USER_ROLE_IDX_NAME);
	}
}
