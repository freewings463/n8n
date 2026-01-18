"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1690787606731-AddMissingPrimaryKeyOnExecutionData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddMissingPrimaryKeyOnExecutionData1690787606731。关键函数/方法:up。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1690787606731-AddMissingPrimaryKeyOnExecutionData.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1690787606731_AddMissingPrimaryKeyOnExecutionData.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

export class AddMissingPrimaryKeyOnExecutionData1690787606731 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE "${tablePrefix}execution_data" ADD PRIMARY KEY("executionId");`,
		);
	}
}
