"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1745934666077-DropRoleTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:DropRoleTable1745934666077。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1745934666077-DropRoleTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1745934666077_DropRoleTable.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

/**
 * Drop the `role` table introduced by `CreateUserManagement1646992772331` and later
 * abandoned with the move to `@n8n/permissions` in https://github.com/n8n-io/n8n/pull/7650
 *
 * Irreversible as there is no use case for restoring a long unused table.
 */
export class DropRoleTable1745934666077 implements IrreversibleMigration {
	async up({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable('role');
	}
}
